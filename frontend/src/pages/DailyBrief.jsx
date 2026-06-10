import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import "../styles/dailyBrief.css";

const MINS_PER_CARD = 1.5;

function DailyBrief() {

  // ── Data ──────────────────────────────────────────────────────────────────
  const [briefData,     setBriefData]     = useState([]);
  const [loading,       setLoading]       = useState(true);
  // Separate map: articleId → { beginner, intermediate, advanced }
  // Updates per-card as each enrichment completes — fixes B/I/A lag
  const [descriptions,  setDescriptions]  = useState({});
  const [enrichingIds,  setEnrichingIds]  = useState(new Set());

  // ── Navigation ────────────────────────────────────────────────────────────
  const [currentIndex,  setCurrentIndex]  = useState(0);
  const navigate = useNavigate();

  // ── Level — auto-select from signup preference ────────────────────────────
  const savedLevel = (localStorage.getItem("userLevel") || "beginner").toLowerCase();
  const normalizedLevel =
    savedLevel.includes("intermediate") ? "intermediate" :
    savedLevel.includes("advanced")     ? "advanced"     : "beginner";
  const [currentLevel, setCurrentLevel] = useState(normalizedLevel);

  // ── Bot ───────────────────────────────────────────────────────────────────
  const [botOpen,     setBotOpen]     = useState(false);
  const [botMessages, setBotMessages] = useState([]);
  const [botInput,    setBotInput]    = useState("");
  const botChatRef = useRef(null);

  // ── Save ──────────────────────────────────────────────────────────────────
  const [savedIds, setSavedIds] = useState(() => {
    const stored = JSON.parse(localStorage.getItem("savedFlashcards") || "[]");
    return new Set(stored.map(a => a.id));
  });

  // ── Completion modal ──────────────────────────────────────────────────────
  const [showCompletion, setShowCompletion] = useState(false);

  // ── Card animation ────────────────────────────────────────────────────────
  const [cardAnim, setCardAnim] = useState("");

  // ==========================================================================
  // FETCH
  // ==========================================================================
  useEffect(() => { fetchBrief(); }, []);

  useEffect(() => {
    if (botChatRef.current)
      botChatRef.current.scrollTop = botChatRef.current.scrollHeight;
  }, [botMessages]);

  async function fetchBrief() {
    setLoading(true);
    try {
      const res  = await fetch("http://127.0.0.1:5000/get-brief");
      const data = await res.json();
      const articles = data.articles || [];
      setBriefData(articles);
      setLoading(false);
      // Enrich each card individually so B/I/A is ready as soon as possible
      articles.forEach(article => enrichOne(article));
    } catch (err) {
      console.error("Brief fetch failed:", err);
      setLoading(false);
    }
  }

  // Enrich a single article — updates descriptions map the moment it's done
  async function enrichOne(article) {
    const id = article.id || article.title;

    setEnrichingIds(prev => new Set(prev).add(id));

    try {
      const res = await fetch("http://127.0.0.1:5000/generate-brief-card", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title:   article.title,
          desc:    article.desc,
          content: article.content || "",
        }),
      });
      const data = await res.json();

      // ✅ Update just this card's descriptions immediately
      setDescriptions(prev => ({ ...prev, [id]: data.card }));

    } catch {
      // Fallback: all levels show raw desc
      setDescriptions(prev => ({
        ...prev,
        [id]: {
          beginner:     article.desc,
          intermediate: article.desc,
          advanced:     article.desc,
        },
      }));
    } finally {
      setEnrichingIds(prev => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  }

  // ==========================================================================
  // SAVE / UNSAVE
  // ==========================================================================
  function toggleSave(article) {
    const id  = article.id || article.title;
    const key = "savedFlashcards";
    let   stored = JSON.parse(localStorage.getItem(key) || "[]");

    if (savedIds.has(id)) {
      // Remove
      stored = stored.filter(a => a.id !== id);
      setSavedIds(prev => { const n = new Set(prev); n.delete(id); return n; });
    } else {
      // Add — store current level description so saved page shows real content
      const cardDesc = descriptions[id]?.[currentLevel] || article.desc;
      stored.push({
        id,
        title:  article.title,
        desc:   cardDesc,
        image:  article.image  || "",
        domain: article.domain || "Brief",
        type:   "flashcard",   // ← lets Saved page put it in the right section
      });
      setSavedIds(prev => new Set(prev).add(id));
    }

    localStorage.setItem(key, JSON.stringify(stored));
  }

  // ==========================================================================
  // NAVIGATION WITH ANIMATION
  // ==========================================================================
  function goToCard(direction) {
    setCardAnim(direction === "next" ? "slide-out-left" : "slide-out-right");
    setTimeout(() => {
      setCurrentIndex(prev => prev + (direction === "next" ? 1 : -1));
      setBotOpen(false);
      setBotMessages([]);
      setCardAnim("slide-in");
    }, 320);
  }

  function handleNext() {
    if (currentIndex === briefData.length - 1) setShowCompletion(true);
    else goToCard("next");
  }

  function handlePrev() {
    if (currentIndex > 0) goToCard("prev");
  }

  // ==========================================================================
  // BOT — same /ask-article as home page (Gemini → Groq fallback)
  // ==========================================================================
  async function sendBotMessage() {
    if (!botInput.trim()) return;

    const userText = botInput.trim();
    setBotInput("");
    setBotMessages(prev => [...prev, { type: "user", text: userText }]);

    try {
      const article = briefData[currentIndex];
      const res = await fetch("http://127.0.0.1:5000/ask-article", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: userText,
          article: {
            title:   article.title,
            desc:    article.desc,
            content: article.content || "",
          },
        }),
      });
      const data = await res.json();
      setBotMessages(prev => [...prev, { type: "ai", text: data.reply }]);
    } catch {
      setBotMessages(prev => [
        ...prev,
        { type: "ai", text: "AI is currently unavailable. Please try again." },
      ]);
    }
  }

  // ==========================================================================
  // DERIVED
  // ==========================================================================
  const article    = briefData[currentIndex];
  const totalCards = briefData.length;
  const progress   = totalCards > 0 ? (((currentIndex + 1) / totalCards) * 100) : 0;
  const estMins    = Math.round(totalCards * MINS_PER_CARD);

  const articleId    = article?.id || article?.title;
  const isEnriching  = enrichingIds.has(articleId);
  const cardDescs    = descriptions[articleId];
  // ✅ Instant switch — reads directly from descriptions map
  const currentDesc  = cardDescs?.[currentLevel] || article?.desc || "";
  const isSaved      = savedIds.has(articleId);

  // ==========================================================================
  // RENDER
  // ==========================================================================
  return (
    <div className="daily-brief-page">
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main className="main-content">
          <div className="brief-container">

            {/* ── HEADER ──────────────────────────────────────────────────── */}
            <div className="brief-top">

              <div className="brief-tag">
                <img src="/images/bolt-1.png" alt="" />
                <span>DAILY 10-MIN NEWS</span>
              </div>

              <div className="brief-header-row">
                <h1 className="feed-title">
                  Today's <span className="highlight-pill">Flashcards</span>
                </h1>
                <div className="card-count">
                  <span className="count-text">
                    {loading ? "—" : `${currentIndex + 1}/${totalCards}`}
                  </span>
                  <span className="count-label">cards</span>
                </div>
              </div>

              <div className="brief-progress-wrapper">
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${progress}%` }} />
                </div>
                <div className="progress-labels">
                  <span>just getting started</span>
                  <span>all caught up</span>
                </div>
              </div>

            </div>

            {/* ── LOADING ─────────────────────────────────────────────────── */}
            {loading && (
              <div className="news-card" style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                <p style={{ fontFamily: "'Space Grotesk', sans-serif", color: "#888", fontSize: "16px" }}>
                  Fetching today's news...
                </p>
              </div>
            )}

            {/* ── CARD ────────────────────────────────────────────────────── */}
            {!loading && article && (
              <div className={`news-card ${cardAnim}`} id="briefCard">

                {/* Image */}
                <div className="card-image">
                  {article.image
                    ? <img src={article.image} alt="" />
                    : <div style={{ width: "100%", height: "100%", background: "linear-gradient(135deg,#3f38e8,#5a54ff)" }} />
                  }
                  <span className="domain-pill">{article.domain}</span>

                  {/* ✅ SAVE BUTTON */}
                  <div
                    className={`save-btn ${isSaved ? "saved" : ""}`}
                    onClick={() => toggleSave(article)}
                    title={isSaved ? "Remove from saved" : "Save flashcard"}
                  >
                    <img src="/images/briefbookmark.png" alt="" />
                  </div>
                </div>

                <div className="card-content">

                  <div className="card-body">
                    <h2 className="card-title">{article.title}</h2>

                    {/* ✅ Shows enriching hint only for THIS card, switches instantly when ready */}
                    {isEnriching
                      ? <p className="card-desc" style={{ color: "#aaa", fontStyle: "italic" }}>
                          Generating explanation...
                        </p>
                      : <p className="card-desc">{currentDesc}</p>
                    }
                  </div>

                  {/* ── ACTIONS ───────────────────────────────────────────── */}
                  <div className="card-actions">

                    {/* B / I / A */}
                    <div className="level-toggle">
                      {["beginner", "intermediate", "advanced"].map(level => (
                        <button
                          key={level}
                          className={`level-btn ${currentLevel === level ? "active" : ""}`}
                          onClick={() => setCurrentLevel(level)}
                          title={level.charAt(0).toUpperCase() + level.slice(1)}
                        >
                          {level[0].toUpperCase()}
                        </button>
                      ))}
                    </div>

                    {/* Ask Bot */}
                    <button
                      className={`chatbot-btn ${botOpen ? "active" : ""}`}
                      onClick={() => setBotOpen(!botOpen)}
                    >
                      <img src="/images/bot.svg" alt="" />
                      <span>Ask Bot</span>
                    </button>

                  </div>

                  {/* ── BOT PANEL ─────────────────────────────────────────── */}
                  <div className={`article-bot ${botOpen ? "show" : ""}`}>

                    <div className="bot-header">
                      <div className="bot-title">
                        <img src="/images/bot-white.png" alt="" />
                        <span>Article Bot</span>
                      </div>
                      <button className="close-bot" onClick={() => setBotOpen(false)}>✕</button>
                    </div>

                    <div className="bot-body">
                      <div className="bot-message">
                        Ask me anything about this flashcard.
                      </div>

                      <div className="bot-chat" ref={botChatRef}>
                        {botMessages.map((msg, i) => (
                          <div key={i} className={`msg ${msg.type}`}>{msg.text}</div>
                        ))}
                      </div>

                      <div className="bot-input">
                        <input
                          type="text"
                          placeholder="Ask about this article..."
                          value={botInput}
                          onChange={e => setBotInput(e.target.value)}
                          onKeyDown={e => e.key === "Enter" && sendBotMessage()}
                        />
                        <button onClick={sendBotMessage}>
                          <img src="/images/send.png" alt="" />
                        </button>
                      </div>
                    </div>

                  </div>

                </div>
              </div>
            )}

            {/* ── PREV / NEXT ──────────────────────────────────────────────── */}
            {!loading && (
              <div className="brief-controls">
                <button
                  className="brief-btn prev"
                  disabled={currentIndex === 0}
                  onClick={handlePrev}
                >
                  ← Prev
                </button>
                <button className="brief-btn next" onClick={handleNext}>
                  {currentIndex === briefData.length - 1 ? "Finish ✓" : "Next →"}
                </button>
              </div>
            )}

            {/* ── COMPLETION MODAL ─────────────────────────────────────────── */}
            {showCompletion && (
              <div className="completion-modal">
                <div className="completion-box">
                  <div style={{ fontSize: "40px" }}>🎉</div>
                  <h2 style={{ fontFamily: "'Syne', sans-serif", fontSize: "35px", fontWeight: 900, margin: "10px 0" }}>
                    You're all caught up!
                  </h2>
                  <p style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "16px", color: "#555", marginTop: "10px" }}>
                    You just crushed {totalCards} stories in under {estMins} minutes. That's actually impressive ngl..
                  </p>
                  <button
                    onClick={() => {
                      setShowCompletion(false);
                      setCurrentIndex(0);
                      setBotOpen(false);
                      setBotMessages([]);
                      setCardAnim("slide-in");
                    }}
                    style={{ marginTop: "25px", padding: "12px 26px", border: "2px solid black", borderRadius: "12px", background: "#D0F248", cursor: "pointer", fontWeight: 600, fontFamily: "'Syne', sans-serif" }}
                  >
                    Review again
                  </button>
                </div>
              </div>
            )}

          </div>
        </main>
      </div>
    </div>
  );
}

export default DailyBrief;