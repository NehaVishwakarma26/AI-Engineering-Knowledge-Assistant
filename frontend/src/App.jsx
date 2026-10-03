import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Something went wrong while connecting to the DevMind server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">D</div>
          <div>
            <h2>DevMind</h2>
            <span>Knowledge Assistant</span>
          </div>
        </div>

        <button className="new-chat" onClick={clearChat}>
          <span>＋</span>
          New conversation
        </button>

        <div className="sidebar-section">
          <p className="section-title">QUICK PROMPTS</p>

          <button
            onClick={() =>
              setQuestion(
                "Explain how hybrid retrieval is implemented in this project."
              )
            }
          >
            🔍 Hybrid retrieval
          </button>

          <button
            onClick={() =>
              setQuestion(
                "Find and explain the RAG pipeline in this project."
              )
            }
          >
            🧠 RAG pipeline
          </button>

          <button
            onClick={() =>
              setQuestion(
                "Explain how the main components of this project are connected."
              )
            }
          >
            🏗️ Project architecture
          </button>
        </div>

        <div className="sidebar-bottom">
          <div className="status">
            <span className="status-dot"></span>
            DevMind online
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="main">
        <header className="header">
          <div>
            <h1>Ask your codebase</h1>
            <p>
              Search, understand and explore your project using DevMind.
            </p>
          </div>

          <div className="model-badge">
            <span></span>
            Ollama
          </div>
        </header>

        {/* Chat */}
        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-icon">✦</div>

              <h2>How can I help you?</h2>

              <p>
                Ask DevMind anything about your codebase. It can inspect your
                project and explain how different components work together.
              </p>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setQuestion(
                      "Find the implementation of hybrid retrieval in this project."
                    )
                  }
                >
                  <strong>Hybrid retrieval</strong>
                  <span>Find dense + BM25 retrieval</span>
                </button>

                <button
                  onClick={() =>
                    setQuestion(
                      "Explain how RRF and reranking are implemented."
                    )
                  }
                >
                  <strong>RRF & reranking</strong>
                  <span>Understand the ranking pipeline</span>
                </button>

                <button
                  onClick={() =>
                    setQuestion(
                      "Explain the architecture of this project."
                    )
                  }
                >
                  <strong>Architecture</strong>
                  <span>Understand the project structure</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-row ${message.role}`}
                >
                  <div className="avatar">
                    {message.role === "user" ? "Y" : "D"}
                  </div>

                  <div className="message">
                    <div className="message-name">
                      {message.role === "user" ? "You" : "DevMind"}
                    </div>

                    <div className="message-content">
                      {message.content}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="avatar">D</div>

                  <div className="message">
                    <div className="message-name">DevMind</div>

                    <div className="typing">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input */}
        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask something about your codebase..."
              rows={1}
            />

            <button
              className="send-button"
              onClick={askQuestion}
              disabled={!question.trim() || loading}
            >
              ↑
            </button>
          </div>

          <p className="input-hint">
            Press Enter to send · Shift + Enter for a new line
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;