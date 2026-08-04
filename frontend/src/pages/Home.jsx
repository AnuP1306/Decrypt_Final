import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import NewsCard from "../components/NewsCard";
import RightSidebar from "../components/RightSidebar";
import { useAuth } from "../context/AuthContext";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../firebase";
import { API_URL } from "../config";

const MINS_PER_CARD = 1.5;

const VIBE_TO_FILTER = {
  "Artificial Intelligence": "ai",
  "Technology": "it",
  "Electronics": "electronics",
};

function Home() {

  const [articles, setArticles]           = useState([]);
  const [visibleCount, setVisibleCount]   = useState(2);
  const [loading, setLoading]             = useState(true);
  const { currentUser } = useAuth();
  const [currentFilter, setCurrentFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  // ── Brief card counts (fetched separately, count-only) ──────────────────
  const [briefCount, setBriefCount] = useState(null); // null = not loaded yet
  const [showCaughtUpModal, setShowCaughtUpModal] = useState(false);
  const [hasShownCaughtUp, setHasShownCaughtUp] = useState(false);
  // const [dismissedCaughtUp, setDismissedCaughtUp] = useState(false);
  const navigate = useNavigate();

  // ── Infinite scroll ──────────────────────────────────────────────────────

  const feedContainerRef = useRef(null);

  useEffect(() => {
    function handleScroll() {
      // Already shown once for this filter — never re-trigger,
      // even if the user is still sitting at/near the bottom.
      if (hasShownCaughtUp) return;

      const container = feedContainerRef.current;
      if (!container) return;

      const containerBottom = container.getBoundingClientRect().bottom;
      const nearBottomOfRenderedCards = containerBottom <= window.innerHeight + 50;

      if (!nearBottomOfRenderedCards) return;

      setVisibleCount(prev => {
        if (prev >= filteredArticles.length && filteredArticles.length > 0) {
          setShowCaughtUpModal(true);
          setHasShownCaughtUp(true);
          return prev;
        }

        return Math.min(prev + 2, filteredArticles.length);
      });
    }

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [articles, currentFilter, hasShownCaughtUp]);

  // ── Fetch home page news ─────────────────────────────────────────────────
  // /get-news always returns instantly now (backend never blocks on
  // GNews). We poll /get-refresh-status briefly after load to detect
  // if a background refresh completes shortly after — if it does, we
  // silently re-fetch the article list so newly-fresh content appears
  // without the user needing to navigate away and back.
  useEffect(() => {
    let pollCount = 0;
    const MAX_POLLS = 6;
    const POLL_INTERVAL_MS = 10000; // 10 seconds
    let lastKnownFinishTime = null;

    async function fetchNews() {
      try {
        const response = await fetch(`${API_URL}/get-news`);
        const data = await response.json();
        setArticles(data.articles || []);
        lastKnownFinishTime = data.refresh_state?.last_run_finished || null;
      } catch (error) {
        console.error("News fetch failed:", error);
      } finally {
        setLoading(false);
      }
    }

    async function pollForRefresh() {
      if (pollCount >= MAX_POLLS) return;
      pollCount++;

      try {
        const res = await fetch(`${API_URL}/get-refresh-status`);
        const status = await res.json();

        const finishedNow = status.last_run_finished;
        const somethingNewArrived =
          finishedNow && finishedNow !== lastKnownFinishTime;

        // if (somethingNewArrived) {
        //   lastKnownFinishTime = finishedNow;
        //   // A background refresh completed since our last fetch —
        //   // pull the updated article list.
        //   const newsRes = await fetch("http://127.0.0.1:5000/get-news");
        //   const newsData = await newsRes.json();
        //   setArticles(newsData.articles || []);
        // }

        if (somethingNewArrived) {
          lastKnownFinishTime = finishedNow;
          const newsRes = await fetch(`${API_URL}/get-news`);
          const newsData = await newsRes.json();
          const freshArticles = newsData.articles || [];

          // Merge by ID instead of replacing the array wholesale. Any
          // article ID already present keeps its EXISTING object
          // reference (and therefore its React key + mounted NewsCard
          // instance + already-generated slides) — only genuinely new
          // article IDs get appended. This is what stops a background
          // refresh from silently re-triggering Gemini calls for cards
          // the user is already looking at.
          setArticles(prevArticles => {
            const existingIds = new Set(prevArticles.map(a => a.id));
            const newOnes = freshArticles.filter(a => !existingIds.has(a.id));

            if (newOnes.length > 0) {
              console.log(`📥 ${newOnes.length} genuinely new articles merged in (existing cards untouched)`);
            } else {
              console.log("📥 Background refresh completed — no new articles to merge, nothing re-rendered");
            }

            return [...prevArticles, ...newOnes];
          });
        }

        if (!status.in_progress && pollCount < MAX_POLLS) {
          setTimeout(pollForRefresh, POLL_INTERVAL_MS);
        } else if (status.in_progress) {
          setTimeout(pollForRefresh, POLL_INTERVAL_MS);
        }
      } catch {
        // Status check failing is non-critical — just stop polling silently.
      }
    }

    fetchNews().then(() => {
      setTimeout(pollForRefresh, POLL_INTERVAL_MS);
    });
  }, []);

  // ── Fetch brief count for the "Today's Brief" card ──────────────────────
  // Uses a lightweight count-only endpoint — does NOT trigger GNews,
  // so opening Home never clashes with Daily Brief's fetch logic.
  useEffect(() => {
    async function fetchBriefCount() {
      try {
        const res  = await fetch(`${API_URL}/get-brief-count`);
        const data = await res.json();
        setBriefCount(data.count ?? 10);
      } catch {
        setBriefCount(10); // safe fallback
      }
    }
    fetchBriefCount();
  }, []);

  useEffect(() => {
    async function loadPreference() {
      if (!currentUser) return;

      const userRef = doc(db, "users", currentUser.uid);
      const snap = await getDoc(userRef);

      if (!snap.exists()) return;

      const vibe = snap.data()?.personalization?.vibe;
      const filter = VIBE_TO_FILTER[vibe];

      if (filter) {
        setCurrentFilter(filter);
      }
    }

    loadPreference();
  }, [currentUser]);

  // ── Derived ──────────────────────────────────────────────────────────────
  const filteredArticles = articles.filter(article => {
    // Filter by category
    const matchesFilter =
      currentFilter === "all" ||
      article.domain?.toLowerCase() === currentFilter.toLowerCase();
  
    // Filter by search
    const query = searchQuery.toLowerCase().trim();
  
    const searchableText = [
      article.title,
      article.summary,
      article.source,
      article.domain,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  
    const keywords = query.split(/\s+/).filter(Boolean);
  
    const matchesSearch =
      query === "" ||
      keywords.every(word => searchableText.includes(word));
  
    return matchesFilter && matchesSearch;
  });

  function handleFilterChange(value) {
    setCurrentFilter(value);
    setVisibleCount(2);
    setShowCaughtUpModal(false);
    setHasShownCaughtUp(false);
  }

  const storyCount = briefCount ?? 10;
  const estMins    = Math.round(storyCount * MINS_PER_CARD);


  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <>
      <Navbar
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery} 
      
      />

      <div className="layout">
        <Sidebar />

        <main className="main-content">
          <div className="home-layout">

            <div className="feed-container" ref={feedContainerRef}>

              <div className="feed-intro">
                <h1 className="feed-title">
                  News that actually{" "}
                  <span className="highlight-text">makes sense</span>
                </h1>
                <p className="feed-subtext">
                  No jargon. No confusion. Just what's happening in the world — explained your way.
                </p>
              </div>

              {/* ── TODAY'S BRIEF CARD ──────────────────────────────────── */}
              <div className="brief-card">
                <div className="brief-left">
                  <img src="/images/logo.svg" className="brief-icon" alt="" />
                  <div>
                    <p className="brief-title">Today's Brief</p>
                    <span className="brief-sub">
                      {briefCount === null
                        ? "Loading stories..."
                        : `${String(storyCount).padStart(2, "0")} stories for you · Est. ${estMins} min read`
                      }
                    </span>
                  </div>
                </div>

                <button
                  className="brief-btn"
                  onClick={() => navigate("/daily-brief")}
                >
                  Start Reading →
                </button>
              </div>

              {/* ── FILTERS ─────────────────────────────────────────────── */}
              <div className="feed-filters">
                {[
                  { label: "All",         value: "all"         },
                  { label: "AI",          value: "ai"          },
                  { label: "IT",          value: "it"          },
                  { label: "Electronics", value: "electronics" },
                ].map(({ label, value }) => (
                  <button
                    key={value}
                    className={`filter ${currentFilter === value ? "active" : ""}`}
                    onClick={() => handleFilterChange(value)}
                  >
                    {label}
                  </button>
                ))}
              </div>

              {/* ── LOADING STATE ───────────────────────────────────────── */}
              {loading && (
                <div style={{ textAlign: "center", padding: "3rem 0" }}>
                  <div
                    style={{
                      width: "32px",
                      height: "32px",
                      margin: "0 auto 14px auto",
                      borderRadius: "50%",
                      border: "3px solid #ece9ff",
                      borderTopColor: "#5b4fe9",
                      animation: "decrypt-spin 0.8s linear infinite",
                    }}
                  />
                  <p style={{ color: "#888", fontSize: "14px", fontFamily: "'Space Grotesk', sans-serif", margin: 0 }}>
                    Fetching today's news...
                  </p>
                  <style>{`
                    @keyframes decrypt-spin {
                      to { transform: rotate(360deg); }
                    }
                  `}</style>
                </div>
              )}

              {/* ── EMPTY STATE ─────────────────────────────────────────── */}
              {!loading && filteredArticles.length === 0 && (
                <div className="empty-state" style={{ textAlign: "center", padding: "2rem", color: "var(--color-text-secondary)" }}>
                  {/* <p>No {currentFilter !== "all" ? currentFilter.toUpperCase() : ""} articles available right now.</p> */}
                  {searchQuery ? (
    <p>No articles found for "{searchQuery}".</p>
) : (
    <p>No {currentFilter !== "all" ? currentFilter.toUpperCase() : ""} articles available right now.</p>
)}
                  <p style={{ fontSize: "0.9rem", marginTop: "0.5rem" }}>
                    Try switching to "All" or check back later.
                  </p>
                </div>
              )}

              {/* ── NEWS CARDS ──────────────────────────────────────────── */}
              {!loading && filteredArticles
                .slice(0, visibleCount)
                .map((article, index) => (
                  <NewsCard
                    key={article.id || index}
                    article={article}
                    index={index}
                    visible={index < visibleCount}
                  />
                ))
              }

              {/* ── ALL CAUGHT UP ─────────────────────────────────────── */}
              {showCaughtUpModal && (
                <div className="completion-modal">
                  <div className="completion-box">
                    <div style={{ fontSize: "40px" }}>🎉</div>
                    <h2 style={{ fontFamily: "'Syne', sans-serif", fontSize: "35px", fontWeight: 900, margin: "10px 0" }}>
                      You're all caught up!
                    </h2>
                    <p style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "16px", color: "#555", marginTop: "10px" }}>
                      You've seen all the {currentFilter !== "all" ? currentFilter.toUpperCase() + " " : ""}
                      stories we have for today. New ones drop soon.
                    </p>
                    <button
                      onClick={() => {
                        setShowCaughtUpModal(false);
                        window.scrollTo({ top: 0, behavior: "smooth" });
                      }}
                      style={{ marginTop: "25px", padding: "12px 26px", border: "2px solid black", borderRadius: "12px", background: "#D0F248", cursor: "pointer", fontWeight: 600, fontFamily: "'Syne', sans-serif" }}
                    >
                      Back to top
                    </button>
                  </div>
                </div>
              )}

            </div>

            <RightSidebar />

          </div>
        </main>
      </div>
    </>
  );
}

export default Home;