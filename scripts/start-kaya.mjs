import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(scriptDir, '..');
const frontendDir = path.join(rootDir, 'frontend');
const isWindows = process.platform === 'win32';
const npmCommand = isWindows ? 'npm.cmd' : 'npm';
const pythonCommand = isWindows ? 'python.exe' : 'python3';
const ollamaCommand = isWindows ? 'ollama.exe' : 'ollama';
const ollamaModel = process.env.KAYA_OLLAMA_MODEL ?? 'qwen2.5:3b';
const ollamaBaseUrl = process.env.KAYA_OLLAMA_BASE_URL ?? 'http://127.0.0.1:11434';
const children = new Set();

function cleanEnv() {
  if (!isWindows) {
    return process.env;
  }

  const env = {};
  for (const [key, value] of Object.entries(process.env)) {
    const normalized = key.toLowerCase();
    const existing = Object.keys(env).find((item) => item.toLowerCase() === normalized);
    if (!existing) {
      env[key] = value;
    }
  }

  return env;
}

function run(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: options.cwd ?? rootDir,
      env: cleanEnv(),
      shell: options.shell ?? false,
      stdio: 'inherit',
    });

    child.on('error', reject);
    child.on('exit', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${command} ${args.join(' ')} exited with code ${code}`));
      }
    });
  });
}

function start(command, args, options = {}) {
  const child = spawn(command, args, {
    cwd: options.cwd ?? rootDir,
    env: cleanEnv(),
    shell: options.shell ?? false,
    stdio: 'inherit',
  });

  children.add(child);
  child.on('exit', () => children.delete(child));
  return child;
}

function openBrowser(url) {
  if (isWindows) {
    spawn('cmd.exe', ['/c', 'start', '', url], { detached: true, stdio: 'ignore' }).unref();
    return;
  }

  const opener = process.platform === 'darwin' ? 'open' : 'xdg-open';
  spawn(opener, [url], { detached: true, stdio: 'ignore' }).unref();
}

async function commandExists(command) {
  const checker = isWindows ? ['where.exe', [command]] : ['which', [command]];
  try {
    await run(checker[0], checker[1]);
    return true;
  } catch {
    return false;
  }
}

async function fetchWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeout ?? 2500);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timeout);
  }
}

async function isOllamaReady() {
  try {
    const response = await fetchWithTimeout(`${ollamaBaseUrl}/api/tags`);
    return response.ok;
  } catch {
    return false;
  }
}

async function prepareOllama() {
  console.log('\nChecking local LLM service...');

  if (!(await commandExists(ollamaCommand))) {
    console.log('Ollama is not installed. KAYA will still run, but open-ended AI replies need Ollama.');
    console.log('Install Ollama and run: ollama pull qwen2.5:3b');
    return;
  }

  if (!(await isOllamaReady())) {
    console.log('Starting Ollama service...');
    start(ollamaCommand, ['serve']);
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }

  if (!(await isOllamaReady())) {
    console.log('Ollama did not become ready. KAYA will use local tools and document fallback for now.');
    return;
  }

  try {
    console.log(`Preparing LLM model ${ollamaModel}...`);
    await run(ollamaCommand, ['pull', ollamaModel]);
  } catch (error) {
    console.log(`Could not prepare ${ollamaModel}: ${error.message}`);
    console.log('KAYA will still start. Pull the model later if needed.');
  }
}

function stopAll() {
  for (const child of children) {
    if (!child.killed) {
      child.kill('SIGTERM');
    }
  }
}

process.on('SIGINT', () => {
  stopAll();
  process.exit(0);
});

process.on('SIGTERM', () => {
  stopAll();
  process.exit(0);
});

console.log('\nStarting KAYA full workspace...\n');

console.log('Checking backend dependencies...');
await run(pythonCommand, ['-m', 'pip', 'install', '-r', path.join('backend', 'requirements.txt')]);

if (!existsSync(path.join(frontendDir, 'node_modules'))) {
  console.log('\nChecking frontend dependencies...');
  await run(npmCommand, ['install'], { cwd: frontendDir, shell: isWindows });
}

await prepareOllama();

console.log('\nLaunching KAYA API on http://127.0.0.1:8000');
const api = start(pythonCommand, [
  '-m',
  'uvicorn',
  'backend.app.main:app',
  '--reload',
  '--host',
  '127.0.0.1',
  '--port',
  '8000',
]);

console.log('Launching KAYA app on http://127.0.0.1:5173\n');
const frontend = start(npmCommand, ['run', 'dev', '--', '--host', '127.0.0.1', '--port', '5173'], {
  cwd: frontendDir,
  shell: isWindows,
});

setTimeout(() => {
  openBrowser('http://127.0.0.1:5173');
}, 5000);

api.on('exit', (code) => {
  if (code !== 0 && code !== null) {
    console.error(`\nKAYA API stopped with code ${code}.`);
  }
  stopAll();
});

frontend.on('exit', (code) => {
  if (code !== 0 && code !== null) {
    console.error(`\nKAYA frontend stopped with code ${code}.`);
  }
  stopAll();
});
