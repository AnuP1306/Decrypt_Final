import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import NewsCard from "../components/NewsCard";
import RightSidebar from "../components/RightSidebar";

const MINS_PER_CARD = 1.5;

function Home() {

  const [articles, setArticles]           = useState([]);
  const [visibleCount, setVisibleCount]   = useState(2);
  const [loading, setLoading]             = useState(true);
  const [currentFilter, setCurrentFilter] = useState("all");

  // ── Brief card counts (fetched separately from /get-brief) ──────────────
  const [briefCount, setBriefCount] = useState(null); // null = not loaded yet
  const navigate = useNavigate();

  // ── Infinite scroll ──────────────────────────────────────────────────────
  useEffect(() => {
    function handleScroll() {
      if (
        window.innerHeight + window.scrollY >=
        document.body.offsetHeight - 300
      ) {
        setVisibleCount(prev => Math.min(prev + 2, articles.length));
      }
    }
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [articles]);

  // ── Fetch home page news ─────────────────────────────────────────────────
  useEffect(() => {
    async function fetchNews() {
      try {
        const response = await fetch("http://127.0.0.1:5000/get-news");
        const data = await response.json();
        setArticles(data.articles || []);
      } catch (error) {
        console.error("News fetch failed:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchNews();
  }, []);

  // ── Fetch brief count for the "Today's Brief" card ──────────────────────
  // We only need the count — a lightweight call that hits the cache on Flask
  useEffect(() => {
    async function fetchBriefCount() {
      try {
        const res  = await fetch("http://127.0.0.1:5000/get-brief");
        const data = await res.json();
        setBriefCount((data.articles || []).length);
      } catch {
        setBriefCount(10); // safe fallback
      }
    }
    fetchBriefCount();
  }, []);

  // ── Derived ──────────────────────────────────────────────────────────────
  const filteredArticles =
    currentFilter === "all"
      ? articles
      : articles.filter(
          a => a.domain?.toLowerCase() === currentFilter
        );

  const storyCount = briefCount ?? 10;
  const estMins    = Math.round(storyCount * MINS_PER_CARD);

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <>
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main className="main-content">
          <div className="home-layout">

            <div className="feed-container">

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
                    {/* Dynamic count and read time */}
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
                    onClick={() => setCurrentFilter(value)}
                  >
                    {label}
                  </button>
                ))}
              </div>

              {/* ── NEWS CARDS ──────────────────────────────────────────── */}
              {!loading && filteredArticles
                .slice(0, visibleCount)
                .map((article, index) => (
                  <NewsCard
                    key={index}
                    article={article}
                    index={index}
                    visible={index < visibleCount}
                  />
                ))
              }

            </div>

            <RightSidebar />

          </div>
        </main>
      </div>
    </>
  );
}

export default Home;