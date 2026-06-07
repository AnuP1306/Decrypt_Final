import { useState, useEffect } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

import NewsCard from "../components/NewsCard";
import RightSidebar from "../components/RightSidebar";

function Home() {

  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    async function fetchNews() {

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/get-news"
        );

        const data = await response.json();
        console.log(data.articles[0]);
        setArticles(data.articles || []);

      } catch (error) {

        console.error(
          "News fetch failed:",
          error
        );

      } finally {

        setLoading(false);

      }
    }

    fetchNews();

  }, []);

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
                  <span className="highlight-text">
                    makes sense
                  </span>
                </h1>

                <p className="feed-subtext">
                  No jargon. No confusion. Just what's happening
                  in the world — explained your way.
                </p>

              </div>

              <div className="brief-card">

                <div className="brief-left">

                  <img
                    src="/images/logo.svg"
                    className="brief-icon"
                    alt=""
                  />

                  <div>

                    <p className="brief-title">
                      Today’s Brief
                    </p>

                    <span className="brief-sub">
                      05 stories for you · Est. 8 min read
                    </span>

                  </div>

                </div>

                <button className="brief-btn">
                  Start Reading →
                </button>

              </div>

              <div className="feed-filters">
                <button className="filter active">
                  All
                </button>

                <button className="filter">
                  AI
                </button>

                <button className="filter">
                  IT
                </button>

                <button className="filter">
                  Electronics
                </button>
              </div>

              {loading ? null : articles.map(
                (article, index) => (
                  <NewsCard
                    key={index}
                    article={article}
                    index={index}
                  />
                )
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