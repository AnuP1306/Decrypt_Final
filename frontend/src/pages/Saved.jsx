import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/saved.css";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Saved() {

  // const [savedArticles,   setSavedArticles]   = useState([]);
  // const [savedFlashcards, setSavedFlashcards] = useState([]);
  const [savedTools, setSavedTools] = useState([]);

  useEffect(() => {
    setSavedArticles(JSON.parse(localStorage.getItem("savedArticles")  || "[]"));
    setSavedFlashcards(JSON.parse(localStorage.getItem("savedFlashcards") || "[]"));
    setSavedTools(
      JSON.parse(localStorage.getItem("savedTools") || "[]")
    );
  }, []);
  const [savedArticles, setSavedArticles] = useState(() =>
  JSON.parse(localStorage.getItem("savedArticles") || "[]")
);

const [savedFlashcards, setSavedFlashcards] = useState(() =>
  JSON.parse(localStorage.getItem("savedFlashcards") || "[]")
);

const [savedOpportunities, setSavedOpportunities] = useState(() =>
  JSON.parse(localStorage.getItem("savedOpportunities") || "[]")
);

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

  function removeTool(id, el) {
    el.style.transform = "scale(0.92)";
    el.style.opacity = "0";
    el.style.transition = "all 0.25s ease";
  
    setTimeout(() => {
      const updated = savedTools.filter(t => t.id !== id);
  
      setSavedTools(updated);
  
      localStorage.setItem(
        "savedTools",
        JSON.stringify(updated)
      );
    }, 250);
  }
  function removeOpportunity(id, el) {
  el.style.transform = "scale(0.92)";
  el.style.opacity = "0";
  el.style.transition = "all 0.25s ease";

  setTimeout(() => {
    const updated = savedOpportunities.filter(
      item => item.id !== id
    );

    setSavedOpportunities(updated);

    localStorage.setItem(
      "savedOpportunities",
      JSON.stringify(updated)
    );
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
            <section className="saved-section">

  <div className="saved-section-header">
    <h2 className="saved-section-title">
      Saved Tools
    </h2>

    <span className="saved-count">
      {savedTools.length} saved
    </span>
  </div>

  <div className="saved-scroll-row">

    {savedTools.length === 0 ? (

      <div className="saved-empty-state">
        <div className="empty-icon">🛠️</div>

        <p>
          No saved tools yet.
          <br />
          Bookmark tools from Tools Library.
        </p>
      </div>

    ) : (

      savedTools.map(tool => (

        <div
          className="saved-card saved-tool-card"
          key={tool.id}
          onClick={() => window.open(tool.url, "_blank")}
          style={{ cursor: "pointer" }}
        >

          <div className="sc-image">

            {tool.image && (
              <img
                src={tool.image}
                alt={tool.name}
              />
            )}

            <span className="sc-domain-pill">
              {tool.category}
            </span>

            <button
              className="sc-unbookmark-btn"
              onClick={(e) =>
                removeTool(
                  tool.id,
                  e.currentTarget.closest(".saved-card")
                )
              }
            >
              <img
                src="/images/briefbookmark.png"
                alt=""
              />
            </button>

          </div>

          <div className="sc-content">
            <h3 className="sc-title">
              {tool.name}
            </h3>

            <p className="sc-desc">
              {tool.description}
            </p>
          </div>

        </div>

      ))

    )}

  </div>

</section>
<section className="saved-section">
              <div className="saved-section-header">
                <h2 className="saved-section-title">
                  Saved Opportunities
                </h2>

                <span className="saved-count">
                  {savedOpportunities.length} saved
                </span>
              </div>

              <div className="saved-scroll-row">

                {savedOpportunities.length === 0 ? (

                  <div className="saved-empty-state">
                    <div className="empty-icon">🎓</div>
                    <p>
                      No saved opportunities yet.
                      <br />
                      Bookmark opportunities from the
                      Opportunities page.
                    </p>
                  </div>

                ) : (

                  savedOpportunities.map((opp) => (

                    <div
                      className="saved-card"
                      key={opp.id}
                    >

                      <div className="sc-image">

                        {opp.image && (
                          <img
                            src={opp.image}
                            alt={opp.title}
                            onError={(e) => {
                              e.target.style.display = "none";
                            }}
                          />
                        )}

                        <span className="sc-domain-pill">
                          {opp.type}
                        </span>

                        <button
                          className="sc-unbookmark-btn"
                          onClick={(e) =>
                            removeOpportunity(
                              opp.id,
                              e.currentTarget.closest(".saved-card")
                            )
                          }
                        >
                          <img
                            src="/images/briefbookmark.png"
                            alt=""
                          />
                        </button>

                      </div>

                      <div className="sc-content">

                        <h3 className="sc-title">
                          {opp.title}
                        </h3>

                        <p className="sc-desc">
                          {opp.company}
                        </p>

                        <span className="sc-flash-badge">
                          🎯 Opportunity
                        </span>

                      </div>

                    </div>

                  ))

                )}

              </div>

            </section>
          </div>
        </main>
      </div>
    </>
  );
}

export default Saved;