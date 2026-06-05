import { useMemo, useState } from 'react';
import Agents from './pages/agents.jsx';
import Chat from './pages/chat.jsx';
import Documents from './pages/documents.jsx';
import Home from './pages/home.jsx';
import Memory from './pages/memory.jsx';
import Settings from './pages/setting.jsx';
import Trainings from './pages/trainings.jsx';

const navItems = [
  { id: 'home', label: 'Home', icon: 'H' },
  { id: 'chat', label: 'Chat', icon: 'C' },
  { id: 'memory', label: 'Memory', icon: 'M' },
  { id: 'agents', label: 'Agents', icon: 'A' },
  { id: 'documents', label: 'Docs', icon: 'D' },
  { id: 'trainings', label: 'Training', icon: 'T' },
  { id: 'settings', label: 'Settings', icon: 'S' },
];

const pages = {
  home: Home,
  chat: Chat,
  memory: Memory,
  agents: Agents,
  documents: Documents,
  trainings: Trainings,
  settings: Settings,
};

export default function App() {
  const [activePage, setActivePage] = useState('home');
  const ActivePage = pages[activePage];

  const pageTitle = useMemo(
    () => navItems.find((item) => item.id === activePage)?.label ?? 'Home',
    [activePage],
  );

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={() => setActivePage('home')} type="button">
          <span className="brand-mark">K</span>
          <span>
            <strong>KAYA</strong>
            <small>Local AI OS</small>
          </span>
        </button>

        <nav aria-label="Primary navigation">
          {navItems.map((item) => (
            <button
              aria-current={activePage === item.id ? 'page' : undefined}
              className="nav-item"
              key={item.id}
              onClick={() => setActivePage(item.id)}
              title={item.label}
              type="button"
            >
              <span aria-hidden="true">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Private workspace</p>
            <h1>{pageTitle}</h1>
          </div>
          <div className="status-pill">
            <span className="status-dot" />
            API ready
          </div>
        </header>
        <ActivePage onNavigate={setActivePage} />
      </main>
    </div>
  );
}
