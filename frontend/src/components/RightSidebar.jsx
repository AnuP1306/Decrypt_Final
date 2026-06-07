import { useState } from "react";

function RightSidebar() {

  const [message, setMessage] = useState("");

  const [chatMessages, setChatMessages] = useState([
    {
      type: "bot",
      text: "Ask me anything about news or tools."
    }
  ]);

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userText = message;

    setChatMessages(prev => [
      ...prev,
      {
        type: "user",
        text: userText
      }
    ]);

    setMessage("");

    try {

      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: userText
        })
      });

      const data = await res.json();

      setChatMessages(prev => [
        ...prev,
        {
          type: "bot",
          text: data.reply
        }
      ]);

    } catch (err) {

      console.error(err);

      setChatMessages(prev => [
        ...prev,
        {
          type: "bot",
          text: "Unable to connect to AI."
        }
      ]);

    }

  };

  return (
    <div className="right-sidebar">

      <div className="rs-card chatbot-card">

        <div className="rs-header">
          <img src="/images/bot.png" alt="" />
          <span>ChatBot</span>
        </div>

        <div className="chat-body">

          {chatMessages.map((msg, index) => (
            <div
              key={index}
              className={`chat-msg ${msg.type}`}
            >
              {msg.text}
            </div>
          ))}

        </div>

        <div className="chat-input">

          <input
            type="text"
            placeholder="Ask me anything..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button onClick={sendMessage}>
            <img src="/images/send.png" alt="" />
          </button>

        </div>

      </div>

      <div className="rs-card">

        <div className="rs-header">
          <img src="/images/bookmark.png" alt="" />
          <span>Saved News</span>
        </div>

        <p className="rs-empty">
          No saved articles yet.
        </p>

        <a href="/saved" className="rs-link">
          View All →
        </a>

      </div>

      <div className="rs-card">

        <div className="rs-header">
          <img src="/images/tools-2.png" alt="" />
          <span>Trending Tools</span>
        </div>

        <div className="tools-grid">

          <div className="tool">
            E
            <span>Elicit</span>
          </div>

          <div className="tool">
            U
            <span>Uizard</span>
          </div>

          <div className="tool">
            C
            <span>Codeium</span>
          </div>

          <div className="tool">
            F
            <span>Flourish</span>
          </div>

          <div className="tool">
            A
            <span>Adobe Podcast</span>
          </div>

          <div className="tool">
            T
            <span>Tome</span>
          </div>

        </div>

      </div>

    </div>
  );
}

export default RightSidebar;