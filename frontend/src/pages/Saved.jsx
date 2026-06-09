// function Saved() {
//     return <h1> saved page </h1>;
//   }
  
//   export default Saved;
import "../styles/saved.css";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Saved() {
  return (
  <>
    <Navbar />

    <div className="layout">

      <Sidebar />

      <main className="main-content saved-main">
      <div className="saved-container">

        <Link to="/home" className="back-btn">
          ← Back
        </Link>

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
            <span className="highlight">
              clean system
            </span>
          </h1>

          <div className="saved-banner">
            Everything you bookmarked, finally in one place...
            Because keeping up with tech is basically a full-time job.
          </div>

        </div>

        {/* SAVED ARTICLES */}

        <section className="saved-section">

          <div className="saved-section-header">
            <h2 className="saved-section-title">
              Saved Articles
            </h2>

            <span className="saved-count">
              0 saved
            </span>
          </div>

          <div className="saved-scroll-row">

            <div className="saved-empty-state">
              <div className="empty-icon">🔖</div>

              <p>
                No saved articles yet.
                <br />
                Bookmark articles from the Home Feed.
              </p>
            </div>

          </div>

        </section>

        {/* SAVED FLASHCARDS */}

        <section className="saved-section">

          <div className="saved-section-header">
            <h2 className="saved-section-title">
              Saved Flashcards
            </h2>

            <span className="saved-count">
              0 saved
            </span>
          </div>

          <div className="saved-scroll-row">

            <div className="saved-empty-state">
              <div className="empty-icon">⚡</div>

              <p>
                No saved flashcards yet.
                <br />
                Bookmark cards from Daily Brief.
              </p>
            </div>

          </div>

              </section>

      </div> {/* saved-container */}

      </main>

    </div> {/* layout */}

  </>
  );
}

export default Saved;