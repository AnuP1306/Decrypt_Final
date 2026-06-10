import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/saved.css";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Saved() {

  const [savedArticles,   setSavedArticles]   = useState([]);
  const [savedFlashcards, setSavedFlashcards] = useState([]);

  useEffect(() => {
    setSavedArticles(JSON.parse(localStorage.getItem("savedArticles")  || "[]"));
    setSavedFlashcards(JSON.parse(localStorage.getItem("savedFlashcards") || "[]"));
  }, []);

  // ── Remove with fade-out animation ──────────────────────────────────────
  function removeArticle(id, el) {
    el.style.transform  = "scale(0.92)";
    el.style.opacity    = "0";
    el.style.transition = "all 0.25s ease";
    setTimeout(() => {
      const updated = savedArticles.filter(a => a.id !== id);
      setSavedArticles(updated);
      localStorage.setItem("savedArticles", JSON.stringify(updated));
    }, 250);
  }

  function removeFlashcard(id, el) {
    el.style.transform  = "scale(0.92)";
    el.style.opacity    = "0";
    el.style.transition = "all 0.25s ease";
    setTimeout(() => {
      const updated = savedFlashcards.filter(a => a.id !== id);
      setSavedFlashcards(updated);
      localStorage.setItem("savedFlashcards", JSON.stringify(updated));
    }, 250);
  }

  return (
    <>
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main className="main-content saved-main">
          <div className="saved-container">

            <Link to="/home" className="back-btn">← Back</Link>

            {/* HERO */}
            <div className="saved-hero">
              <div className="saved-mini-header">
                <div className="saved-icon-box">
                  <img src="/images/saved.png" alt="Saved" />
                </div>
                <span>YOUR COLLECTION</span>
              </div>

              <h1 className="saved-title">
                Your saved chaos is now a
                <br />
                <span className="highlight">clean system</span>
              </h1>

              <div className="saved-banner">
                Everything you bookmarked, finally in one place...
                Because keeping up with tech is basically a full-time job.
              </div>
            </div>

            {/* ── SAVED ARTICLES ─────────────────────────────────────── */}
            <section className="saved-section">
              <div className="saved-section-header">
                <h2 className="saved-section-title">Saved Articles</h2>
                <span className="saved-count" id="articleCount">
                  {savedArticles.length} saved
                </span>
              </div>

              <div className="saved-scroll-row" id="savedArticlesRow">

                {savedArticles.length === 0
                  ? (
                    <div className="saved-empty-state" id="articlesEmpty">
                      <div className="empty-icon">🔖</div>
                      <p>No saved articles yet.<br />Bookmark articles from the Home Feed.</p>
                    </div>
                  )
                  : savedArticles.map(article => (
                    <div
                      className="saved-card saved-article-card"
                      key={article.id}
                      data-id={article.id}
                    >
                      <div className="sc-image">
                        {article.image && (
                          <img
                            src={article.image}
                            alt={article.title}
                            onError={e => { e.target.parentElement.style.background = "linear-gradient(135deg,#3f38e8,#5a54ff)"; e.target.style.display = "none"; }}
                          />
                        )}
                        <span className="sc-domain-pill">{article.domain || "NEWS"}</span>
                        <button
                          className="sc-unbookmark-btn"
                          title="Unsave"
                          onClick={e => removeArticle(article.id, e.currentTarget.closest(".saved-card"))}
                        >
                          <img src="/images/briefbookmark.png" alt="" />
                        </button>
                      </div>
                      <div className="sc-content">
                        <h3 className="sc-title">{article.title}</h3>
                        <p className="sc-desc">{article.desc || ""}</p>
                      </div>
                    </div>
                  ))
                }
              </div>
            </section>

            {/* ── SAVED FLASHCARDS ───────────────────────────────────── */}
            <section className="saved-section">
              <div className="saved-section-header">
                <h2 className="saved-section-title">Saved Flashcards</h2>
                <span className="saved-count" id="flashcardCount">
                  {savedFlashcards.length} saved
                </span>
              </div>

              <div className="saved-scroll-row" id="savedFlashcardsRow">

                {savedFlashcards.length === 0
                  ? (
                    <div className="saved-empty-state" id="flashcardsEmpty">
                      <div className="empty-icon">⚡</div>
                      <p>No saved flashcards yet.<br />Bookmark cards from Daily Brief.</p>
                    </div>
                  )
                  : savedFlashcards.map(card => (
                    <div
                      className="saved-card saved-flashcard-card"
                      key={card.id}
                      data-id={card.id}
                    >
                      <div className="sc-image sc-image-flash">
                        {card.image && (
                          <img
                            src={card.image}
                            alt={card.title}
                            onError={e => { e.target.parentElement.style.background = "linear-gradient(135deg,#3f38e8,#5a54ff)"; e.target.style.display = "none"; }}
                          />
                        )}
                        <span className="sc-domain-pill">{card.domain || "BRIEF"}</span>
                        <button
                          className="sc-unbookmark-btn"
                          title="Unsave"
                          onClick={e => removeFlashcard(card.id, e.currentTarget.closest(".saved-card"))}
                        >
                          <img src="/images/briefbookmark.png" alt="" />
                        </button>
                      </div>
                      <div className="sc-content">
                        <h3 className="sc-title">{card.title}</h3>
                        <p className="sc-desc">{card.desc || ""}</p>
                        <span className="sc-flash-badge">⚡ Flashcard</span>
                      </div>
                    </div>
                  ))
                }
              </div>
            </section>

          </div>
        </main>
      </div>
    </>
  );
}

export default Saved;