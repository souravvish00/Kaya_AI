import { useState } from "react";

type Message = {
  role: "assistant" | "user";
  content: string;
};

export default function App() {

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello 👋 I am OpenJarvis. How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");

  const sendMessage = () => {

    if (!input.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentInput = input;

    setInput("");

    setTimeout(() => {

      const aiMessage: Message = {
        role: "assistant",
        content:
          "This is a demo AI response for: " +
          currentInput,
      };

      setMessages((prev) => [...prev, aiMessage]);

    }, 700);
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="logo">
          OpenJarvis
        </div>

        <button className="new-chat-btn">
          + New Chat
        </button>

        <div className="history">

          <div className="history-item">
            AI Assistant
          </div>

          <div className="history-item">
            Python Help
          </div>

          <div className="history-item">
            Data Analysis
          </div>

        </div>

      </aside>

      {/* Main Chat */}
      <main className="chat-container">

        <div className="chat-header">
          OpenJarvis AI
        </div>

        <div className="messages">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={`message ${msg.role}`}
            >

              <div className="message-content">
                {msg.content}
              </div>

            </div>

          ))}

        </div>

        {/* Input Area */}
        <div className="input-area">

          <input
            type="text"
            placeholder="Send a message..."
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button onClick={sendMessage}>
            Send
          </button>

        </div>

      </main>

    </div>
  );
}