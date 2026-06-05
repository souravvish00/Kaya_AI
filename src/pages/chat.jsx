import { useMemo, useState } from 'react';

const starterPrompts = [
  'Explain quantum computing simply.',
  'Search style: best way to train this assistant.',
  'Create a perfect support reply for an angry customer.',
];

const apiFetch = async (path, options) => {
  try {
    return await fetch(path, options);
  } catch (proxyError) {
    return fetch(`http://127.0.0.1:8000${path}`, options);
  }
};

export default function Chat() {
  const [message, setMessage] = useState('');
  const [mode, setMode] = useState('assistant');
  const [sessionId, setSessionId] = useState('');
  const [saveTraining, setSaveTraining] = useState(false);
  const [chat, setChat] = useState([
    {
      role: 'assistant',
      content:
        'Hi, I am KAYA. I can help with chat, books/data, training examples, and grade-12 math. Ask me naturally, like 56+98 or solve quadratic x^2 - 5x + 6 = 0.',
    },
  ]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState('');

  const lastExchange = useMemo(() => {
    const lastAssistant = [...chat].reverse().find((item) => item.role === 'assistant');
    const lastUser = [...chat].reverse().find((item) => item.role === 'user');
    return lastUser && lastAssistant ? { prompt: lastUser.content, completion: lastAssistant.content } : null;
  }, [chat]);

  const sendMessage = async (text = message) => {
    const trimmed = text.trim();
    if (!trimmed || isSending) return;

    setError('');
    setIsSending(true);
    setChat((items) => [...items, { role: 'user', content: trimmed }]);
    setMessage('');

    try {
      const response = await apiFetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: trimmed,
          session_id: sessionId || null,
          mode,
          save_training: saveTraining,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with ${response.status}`);
      }

      const data = await response.json();
      setSessionId(data.session_id);
      setChat((items) => [...items, { role: 'assistant', content: data.response }]);
    } catch (requestError) {
      setError(requestError.message);
      setChat((items) => [
        ...items,
        {
          role: 'assistant',
          content: 'I could not reach my local KAYA API. Start the backend, then I can chat, solve math, and read your uploaded data.',
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const saveLastExchange = async () => {
    if (!lastExchange) return;
    setError('');
    try {
      const response = await apiFetch('/api/training/examples', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...lastExchange, tags: ['manual-chat'], rating: 5 }),
      });
      if (!response.ok) throw new Error(`Save failed with ${response.status}`);
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  return (
    <section className="chat-layout">
      <div className="chat-panel">
        <div className="chat-tools">
          <div className="segmented-control" aria-label="Chat mode">
            {['assistant', 'search', 'trainer'].map((item) => (
              <button
                aria-pressed={mode === item}
                key={item}
                onClick={() => setMode(item)}
                type="button"
              >
                {item}
              </button>
            ))}
          </div>
          <label className="training-toggle">
            <input
              checked={saveTraining}
              onChange={(event) => setSaveTraining(event.target.checked)}
              type="checkbox"
            />
            Save replies for training
          </label>
        </div>

        <div className="message-list" aria-live="polite">
          {chat.map((item, index) => (
            <article className={`message ${item.role}`} key={`${item.role}-${index}`}>
              <span>{item.role === 'user' ? 'You' : 'KAYA'}</span>
              <p>{item.content}</p>
            </article>
          ))}
        </div>

        <form
          className="composer"
          onSubmit={(event) => {
            event.preventDefault();
            sendMessage();
          }}
        >
          <input
            aria-label="Message"
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Ask KAYA anything..."
            value={message}
          />
          <button disabled={isSending || !message.trim()} type="submit">
            {isSending ? 'Sending' : 'Send'}
          </button>
        </form>
        <div className="chat-actions">
          <button className="secondary" disabled={!lastExchange} onClick={saveLastExchange} type="button">
            Save last reply as training data
          </button>
          <button
            className="secondary"
            onClick={() => {
              setChat([
                {
                  role: 'assistant',
                  content: 'New chat started. I am ready to learn from your questions and data.',
                },
              ]);
              setSessionId('');
            }}
            type="button"
          >
            New chat
          </button>
        </div>
        {error ? <p className="inline-error">{error}</p> : null}
      </div>

      <aside className="side-panel">
        <h2>Google-Type Flow</h2>
        <p>
          Use Search mode for direct answer blocks. Use Trainer mode to design datasets,
          fine-tuning steps, and evaluation prompts.
        </p>
        <div className="prompt-list">
          {starterPrompts.map((prompt) => (
            <button key={prompt} onClick={() => sendMessage(prompt)} type="button">
              {prompt}
            </button>
          ))}
        </div>
        <div className="session-box">
          <span>Session</span>
          <code>{sessionId || 'new'}</code>
        </div>
      </aside>
    </section>
  );
}
