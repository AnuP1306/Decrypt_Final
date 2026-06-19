// import { useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";

// import Navbar from "../components/Navbar";
// import Sidebar from "../components/Sidebar";
// import NewsCard from "../components/NewsCard";
// import RightSidebar from "../components/RightSidebar";

// const MINS_PER_CARD = 1.5;

// function Home() {

//   const [articles, setArticles]           = useState([]);
//   const [visibleCount, setVisibleCount]   = useState(2);
//   const [loading, setLoading]             = useState(true);
//   const [currentFilter, setCurrentFilter] = useState("all");

//   // ── Brief card counts (fetched separately from /get-brief) ──────────────
//   const [briefCount, setBriefCount] = useState(null); // null = not loaded yet
//   const navigate = useNavigate();

//   // ── Infinite scroll ──────────────────────────────────────────────────────
//   useEffect(() => {
//     function handleScroll() {
//       if (
//         window.innerHeight + window.scrollY >=
//         document.body.offsetHeight - 300
//       ) {
//         setVisibleCount(prev => Math.min(prev + 2, articles.length));
//       }
//     }
//     window.addEventListener("scroll", handleScroll);
//     return () => window.removeEventListener("scroll", handleScroll);
//   }, [articles]);

//   // ── Fetch home page news ─────────────────────────────────────────────────
//   useEffect(() => {
//     async function fetchNews() {
//       try {
//         const response = await fetch("http://127.0.0.1:5000/get-news");
//         const data = await response.json();
//         setArticles(data.articles || []);
//       } catch (error) {
//         console.error("News fetch failed:", error);
//       } finally {
//         setLoading(false);
//       }
//     }
//     fetchNews();
//   }, []);

//   // ── Fetch brief count for the "Today's Brief" card ──────────────────────
//   // We only need the count — a lightweight call that hits the cache on Flask
//   useEffect(() => {
//     async function fetchBriefCount() {
//       try {
//         const res  = await fetch("http://127.0.0.1:5000/get-brief");
//         const data = await res.json();
//         setBriefCount((data.articles || []).length);
//       } catch {
//         setBriefCount(10); // safe fallback
//       }
//     }
//     fetchBriefCount();
//   }, []);

//   // ── Derived ──────────────────────────────────────────────────────────────
//   const filteredArticles =
//     currentFilter === "all"
//       ? articles
//       : articles.filter(
//           a => a.domain?.toLowerCase() === currentFilter
//         );

//   const storyCount = briefCount ?? 10;
//   const estMins    = Math.round(storyCount * MINS_PER_CARD);

//   // ── Render ───────────────────────────────────────────────────────────────
//   return (
//     <>
//       <Navbar />

//       <div className="layout">
//         <Sidebar />

//         <main className="main-content">
//           <div className="home-layout">

//             <div className="feed-container">

//               <div className="feed-intro">
//                 <h1 className="feed-title">
//                   News that actually{" "}
//                   <span className="highlight-text">makes sense</span>
//                 </h1>
//                 <p className="feed-subtext">
//                   No jargon. No confusion. Just what's happening in the world — explained your way.
//                 </p>
//               </div>

//               {/* ── TODAY'S BRIEF CARD ──────────────────────────────────── */}
//               <div className="brief-card">
//                 <div className="brief-left">
//                   <img src="/images/logo.svg" className="brief-icon" alt="" />
//                   <div>
//                     <p className="brief-title">Today's Brief</p>
//                     {/* Dynamic count and read time */}
//                     <span className="brief-sub">
//                       {briefCount === null
//                         ? "Loading stories..."
//                         : `${String(storyCount).padStart(2, "0")} stories for you · Est. ${estMins} min read`
//                       }
//                     </span>
//                   </div>
//                 </div>

//                 <button
//                   className="brief-btn"
//                   onClick={() => navigate("/daily-brief")}
//                 >
//                   Start Reading →
//                 </button>
//               </div>

//               {/* ── FILTERS ─────────────────────────────────────────────── */}
//               <div className="feed-filters">
//                 {[
//                   { label: "All",         value: "all"         },
//                   { label: "AI",          value: "ai"          },
//                   { label: "IT",          value: "it"          },
//                   { label: "Electronics", value: "electronics" },
//                 ].map(({ label, value }) => (
//                   <button
//                     key={value}
//                     className={`filter ${currentFilter === value ? "active" : ""}`}
//                     onClick={() => setCurrentFilter(value)}
//                   >
//                     {label}
//                   </button>
//                 ))}
//               </div>

//               {/* ── NEWS CARDS ──────────────────────────────────────────── */}
//               {!loading && filteredArticles
//                 .slice(0, visibleCount)
//                 .map((article, index) => (
//                   <NewsCard
//                     key={index}
//                     article={article}
//                     index={index}
//                     visible={index < visibleCount}
//                   />
//                 ))
//               }

//             </div>

//             <RightSidebar />

//           </div>
//         </main>
//       </div>
//     </>
//   );
// }

// export default Home;

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import NewsCard from "../components/NewsCard";
import RightSidebar from "../components/RightSidebar";
import { useAuth } from "../context/AuthContext";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../firebase";

const MINS_PER_CARD = 1.5;

const VIBE_TO_FILTER = {
  "Artificial Intelligence": "ai",
  "Technology": "it",
  "Electronics": "electronics",
};


// Map signup domain values → filter values used by the feed.
// Adjust keys to match whatever your auth flow stores in localStorage.
// const DOMAIN_FILTER_MAP = {
//   ai:          "ai",
//   it:          "it",
//   electronics: "electronics",
//   AI:          "ai",
//   IT:          "it",
//   Electronics: "electronics",
// };

// function getDefaultFilter() {
//   // Respect the domain the user chose at signup (stored by auth flow)
//   const userDomain = localStorage.getItem("userDomain");
//   if (userDomain && DOMAIN_FILTER_MAP[userDomain]) {
//     return DOMAIN_FILTER_MAP[userDomain];
//   }
//   // Guest users see only AI domain 
//   return "ai";
// }

function Home() {

  const [articles, setArticles]           = useState([]);
  const [visibleCount, setVisibleCount]   = useState(2);
  const [loading, setLoading]             = useState(true);
  const { currentUser } = useAuth();
  // const [currentFilter, setCurrentFilter] = useState(getDefaultFilter);
  const [currentFilter, setCurrentFilter] =
  useState("all");

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
        setVisibleCount(prev => Math.min(prev + 2, filteredArticles.length));
      }
    }
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [articles, currentFilter]);

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

  useEffect(() => {
    async function loadPreference() {
      if (!currentUser) return;
  
      const userRef = doc(db, "users", currentUser.uid);
      const snap = await getDoc(userRef);
  
      if (!snap.exists()) return;
  
      const vibe =
        snap.data()?.personalization?.vibe;
  
      const filter =
        VIBE_TO_FILTER[vibe];
  
      if (filter) {
        setCurrentFilter(filter);
      }
    }
  
    loadPreference();
  }, [currentUser]);

  // ── Derived ──────────────────────────────────────────────────────────────
  // Normalize domain to lowercase for comparison so "AI", "ai", "Ai" all match
  const filteredArticles =
    currentFilter === "all"
      ? articles
      : articles.filter(
          a => a.domain?.toLowerCase() === currentFilter.toLowerCase()
        );

  const allCaughtUp =
    !loading &&
    filteredArticles.length > 0 &&
    visibleCount >= filteredArticles.length;

  const storyCount = briefCount ?? 10;
  const estMins    = Math.round(storyCount * MINS_PER_CARD);

  // ── Reset visible count whenever filter changes ───────────────────────────
  function handleFilterChange(value) {
    setCurrentFilter(value);
    setVisibleCount(2);
  }

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

              {/* ── EMPTY STATE ─────────────────────────────────────────── */}
              {!loading && filteredArticles.length === 0 && (
                <div className="empty-state" style={{ textAlign: "center", padding: "2rem", color: "var(--color-text-secondary)" }}>
                  <p>No {currentFilter !== "all" ? currentFilter.toUpperCase() : ""} articles available right now.</p>
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

              {/* ── ALL CAUGHT UP ───────────────────────────────────────── */}
              {allCaughtUp && (
                <div className="caught-up-card">
                  <div className="caught-up-icon">🎉</div>
                  <h3 className="caught-up-title">You're all caught up!</h3>
                  <p className="caught-up-sub">
                    You've seen all the {currentFilter !== "all" ? currentFilter.toUpperCase() + " " : ""}
                    stories we have for today. Check back later for more.
                  </p>
                  <button
                    className="caught-up-btn"
                    onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
                  >
                    Back to top
                  </button>
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