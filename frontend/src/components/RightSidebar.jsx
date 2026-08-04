import { useState, useEffect } from "react";
import { API_URL } from "../config";

function RightSidebar() {

  const [message, setMessage] = useState("");
  const [sidebarTools, setSidebarTools] = useState([]);

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

  useEffect(() => {
    async function loadTools() {
      try {
        const res = await fetch( `${ API_URL }/get-tools`);
        const data = await res.json();
  
        if (!data.tools) return;
  
        // Only fresh tools
        const liveTools = data.tools.filter(
          tool =>
            tool.source === "producthunt" ||
            tool.source === "hackernews"
        );

        const categories = new Set();
const selected = [];

for (const tool of liveTools) {

  if (!categories.has(tool.category)) {

    categories.add(tool.category);
    selected.push(tool);

  }

  if (selected.length === 6) break;
}

if (selected.length < 6) {

  for (const tool of data.tools) {

    if (selected.find(t => t.id === tool.id))
      continue;

    selected.push(tool);

    if (selected.length === 6)
      break;
  }

}

setSidebarTools(selected);
  
        // If not enough live tools, fill with fallback
        // const tools =
        //   liveTools.length >= 6
        //     ? liveTools.slice(0, 6)
        //     : data.tools.slice(0, 6);
  
        // setSidebarTools(tools);
  
      } catch (err) {
        console.error("Couldn't load sidebar tools", err);
      }
    }
  
    loadTools();
  }, []);

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

  {sidebarTools.map(tool => (

    <div
      key={tool.id}
      className="tool"
      onClick={() => window.open(tool.url, "_blank")}
      title={tool.name}
    >

      {tool.name.charAt(0).toUpperCase()}

      <span>
  {tool.name.length > 18
    ? tool.name.substring(0, 18) + "..."
    : tool.name}
</span>

    </div>

  ))}

</div>

      </div>

    </div>
  );
}

export default RightSidebar;