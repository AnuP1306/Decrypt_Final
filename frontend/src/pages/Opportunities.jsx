// function Opportunities() {
//     return <h1> Opportunities </h1>;
//   }
  
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import "../styles/opportunities.css";
import { opportunities } from "../data/opportunitiesData";


function Opportunities() {
    const navigate = useNavigate();

  const [selectedFilter, setSelectedFilter] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [showToast, setShowToast] = useState(false);
 

  const filters = [
    "All",
    "Student Perks",
    "Courses",
    "Workshops",
  ];

  const filteredOpportunities = opportunities.filter((opp) => {
    const matchesFilter =
      selectedFilter === "All" ||
      opp.type === selectedFilter;

    const matchesSearch =
      opp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      opp.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      opp.desc.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  const handleAlerts = () => {
    setShowToast(true);

    setTimeout(() => {
      setShowToast(false);
    }, 2500);
  };

  return (
    <>
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main className="main-content">
          <div className="opp-page">
            <div className="opp-container">

              {/* BACK BUTTON */}

           <button
  className="back-btn"
  onClick={() => navigate("/home")}
>
  ← Back
</button>

              {/* MINI HEADER */}

              <div className="opp-mini-header">
               <div className="opp-icon-box">
                <img
              src="/images/opportunity.png"
              alt="Student Opportunities"
              />
              </div>

                <span className="opp-mini-text">
                  STUDENT OPPORTUNITIES
                </span>
              </div>

              {/* TITLE */}

              <h1>
                Your student ID is a{" "}
                <span className="highlight">
                  VIP pass
                </span>
              </h1>

              <p>
                All the perks, grants, and internships your seniors gatekept. Free tools, stipends, and career boosts —
                all student-exclusive.
              </p>

              {/* BANNER */}

              <div className="opp-banner">
                All listings require proof of student status
                (student ID or .edu email).
                Bookmark this page and check back weekly.
              </div>

              {/* SEARCH */}

              <div className="opp-search">
                <input
                  type="text"
                  placeholder="search opportunities..."
                  value={searchTerm}
                  onChange={(e) =>
                    setSearchTerm(e.target.value)
                  }
                />
              </div>

              {/* FILTERS */}

              <div className="opp-filters">
                {filters.map((filter) => (
                  <button
                    key={filter}
                    className={
                      selectedFilter === filter
                        ? "active"
                        : ""
                    }
                    onClick={() =>
                      setSelectedFilter(filter)
                    }
                  >
                    {filter}
                  </button>
                ))}
              </div>

              {/* OPPORTUNITY LIST */}

              <div className="opp-list">
                {filteredOpportunities.map((opp) => (
                  <div
                    key={opp.id}
                    className="opp-card"
                  >
                    <div className="opp-image">
                      <img
                        src={opp.image}
                        alt={opp.title}
                      />
                    </div>

                    <div className="opp-content">
                      <div className="opp-tags">
                        <span className="tag primary">
                          {opp.type}
                        </span>

                        <span className="tag outline">
                          Student ID Required
                        </span>
                      </div>

                      <h3>{opp.title}</h3>

                      <p className="company">
                        {opp.company}
                      </p>

                      <p className="desc">
                        {opp.desc}
                      </p>

                      <div className="meta">
                        <span>
                          📅 {opp.deadline}
                        </span>

                        <span>
                          📍 {opp.location}
                        </span>

                        {opp.stipend && (
                          <span>
                            💰 {opp.stipend}
                          </span>
                        )}
                      </div>

                      <div className="tags">
                        {opp.tags.map(
                          (tag, index) => (
                            <span key={index}>
                              #{tag}
                            </span>
                          )
                        )}
                      </div>

                      <a
                        href={opp.link}
                        target="_blank"
                        rel="noreferrer"
                        className="apply-btn"
                      >
                        Apply Now ↗
                      </a>
                    </div>
                  </div>
                ))}
              </div>

              {/* CTA */}

              <div className="opp-cta">
                <div>
                  <h3>
                    Get new opportunities in your feed
                  </h3>

                  <p>
                    D-Bot monitors 50+ sources daily.
                  </p>
                </div>

                <button onClick={handleAlerts}>
                  Turn on alerts
                </button>
              </div>

              {/* TOAST */}

              <div
                className={`toast ${
                  showToast ? "show" : ""
                }`}
              >
                🔔 Alerts turned on!
              </div>

            </div>
          </div>
        </main>
      </div>
    </>
  );
}

export default Opportunities;