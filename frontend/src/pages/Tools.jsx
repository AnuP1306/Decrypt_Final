import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import "../styles/tools.css";

const FILTERS = [
  { label: "All", value: "all" },
  { label: "AI Agents", value: "AI Agents" },
  { label: "LLMs", value: "LLMs" },
  { label: "Developer Tools", value: "Developer Tools" },
  { label: "Engineering", value: "Engineering & Development" },
  { label: "Design", value: "Design & Creative" },
  { label: "Productivity", value: "Productivity" },
  { label: "Marketing", value: "Marketing & Sales" },
  { label: "Health", value: "Health & Wellness" },
];

const CAT_GRADIENTS = {
  "AI":                "linear-gradient(135deg,#3f38e8,#7c3aed)",
  "Developer Tools":   "linear-gradient(135deg,#0f172a,#1e40af)",
  "Design":            "linear-gradient(135deg,#db2777,#f97316)",
  "Productivity":      "linear-gradient(135deg,#059669,#0891b2)",
  "Security":          "linear-gradient(135deg,#1e293b,#334155)",
  "Finance":           "linear-gradient(135deg,#047857,#065f46)",
  "Health & Wellness": "linear-gradient(135deg,#0d9488,#10b981)",
  "Education":         "linear-gradient(135deg,#7c3aed,#4f46e5)",
};

const SOURCE_LABEL = {
  producthunt: "PH",
  hackernews:  "HN",
};

// ── Single card ───────────────────────────────────────────────────────────────
function ToolCard({ tool }) {
  const [imgFailed, setImgFailed] = useState(false);

  const [saved, setSaved] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("savedTools") || "[]")
        .some(t => t.id === tool.id);
    } catch { return false; }
  });

  const hasBanner = typeof tool.image === "string"
    && tool.image.trim() !== ""
    && !imgFailed;

  const gradient = CAT_GRADIENTS[tool.category] || CAT_GRADIENTS["AI"];
  const initial  = (tool.name || "?")[0].toUpperCase();
  const badge    = SOURCE_LABEL[tool.source] || null;

  function toggleSave(e) {
    e.preventDefault();
    e.stopPropagation();
    try {
      let list = JSON.parse(localStorage.getItem("savedTools") || "[]");
      if (saved) {
        list = list.filter(t => t.id !== tool.id);
      } else {
        if (!list.find(t => t.id === tool.id)) list.push({
          id: tool.id,
          name: tool.name,
          description: tool.description,
          image: tool.image,
          favicon: tool.favicon,
          category: tool.category,
          url: tool.url
        });;
      }
      localStorage.setItem("savedTools", JSON.stringify(list));
    } catch {}
    setSaved(s => !s);
  }

  return (
    <div className="card" data-category={tool.category}>

      {/* ── Image / gradient header ── */}
      <div
        className="card-img"
        style={hasBanner ? {} : { background: gradient }}
      >
        {hasBanner && (
          <img
            src={tool.image}
            alt={tool.name}
            onError={() => setImgFailed(true)}
          />
        )}

        {/* Shown when no banner: big initial letter on gradient */}
        {/* {!hasBanner && (
          <div className="card-initial">{initial}</div>
        )} */}

{!hasBanner && tool.favicon ? (
  <div className="card-favicon">
    <img
      src={tool.favicon}
      alt=""
      onError={(e) => {
        e.target.style.display = "none";
      }}
    />
  </div>
) : !hasBanner ? (
  <div className="card-initial">{initial}</div>
) : null}

        {/* Save icon — top right */}
        <button
          className={`save-icon-btn ${saved ? "saved" : ""}`}
          onClick={toggleSave}
          title={saved ? "Unsave" : "Save"}
        >
          <svg viewBox="0 0 24 24"
               fill={saved ? "currentColor" : "none"}
               stroke="currentColor" strokeWidth="2.2"
               width="15" height="15">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
          </svg>
        </button>

        {/* Pills — bottom left */}
        <div className="tags-top">
          <span className="tag free">{tool.is_free ? "FREE" : "PAID"}</span>
          <span className="tag category">{tool.category}</span>
          {badge && (
            <span className="tag source-badge">{badge}</span>
          )}
        </div>
      </div>

      {/* ── Body ── */}
      <div className="card-body">
        <h3>{tool.name}</h3>
        <p>{tool.description}</p>

        <div className="hashtags">
          {(tool.tags || []).filter(Boolean).map(tag => (
            <span key={tag}>{tag}</span>
          ))}
        </div>

        <a href={tool.url} target="_blank" rel="noreferrer" className="btn">
          Check it out ↗
        </a>
      </div>

    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
export default function Tools() {
  const navigate = useNavigate();
  const [tools,   setTools]   = useState([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(false);
  const [filter,  setFilter]  = useState("all");
  const [search,  setSearch]  = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get-tools")
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(d => { setTools(Array.isArray(d.tools) ? d.tools : []); setError(false); })
      .catch(() => { setError(true); setTools([]); })
      .finally(() => setLoading(false));
  }, []);

  const visible = tools.filter(t => {
    const matchCat    = filter === "all" || t.category === filter;
    const q           = search.toLowerCase().trim();
    const matchSearch = !q
      || (t.name        || "").toLowerCase().includes(q)
      || (t.description || "").toLowerCase().includes(q)
      || (t.category    || "").toLowerCase().includes(q)
      || (t.tags        || []).some(tag => tag.toLowerCase().includes(q));
    return matchCat && matchSearch;
  });

  const totalTools  = tools.length;
  const freeCount   = tools.filter(t => t.is_free).length;
  const freePercent = totalTools > 0 ? Math.round((freeCount / totalTools) * 100) : 0;
  const liveCount   = tools.filter(t => t.source === "producthunt" || t.source === "hackernews").length;

  return (
    <>
      <Navbar />
      <div className="layout">
        <Sidebar />
        <main className="main-content">
          <div className="tools-page">
            <div className="tools-header">

              <button className="back-btn" onClick={() => navigate("/home")}>← Back</button>

              <div className="top-label">
                <span className="icon"><img src="/images/wrench.png" alt="tool" /></span>
                TOOLS LIBRARY
              </div>

              <h1 className="page-title">
                AI tools that actually <span className="heighlight">go hard</span>
              </h1>
              <p className="page-subtitle">
                The lesser-known, criminally underrated AI tools and sites. Free stuff
                prioritized. Your LinkedIn bio is about to level up.
              </p>

              <div className="stats">
                <div className="card2">
                  <h2>{loading ? "..." : `${totalTools}+`}</h2>
                  <p>Tools Listed</p>
                </div>
                <div className="card2">
                  <h2>{loading ? "..." : `${freePercent}%`}</h2>
                  <p>Free Tools</p>
                </div>
                <div className="card2">
                  <h2>{loading ? "..." : liveCount > 0 ? liveCount : "Daily"}</h2>
                  <p>{liveCount > 0 ? "Live Picks" : "Updated"}</p>
                </div>
              </div>

              <div className="search-box">
                <input
                  type="text"
                  placeholder="Search tools..."
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                />
              </div>

              <div className="categories">
                {FILTERS.map(f => (
                  <button
                    key={f.value}
                    className={filter === f.value ? "active" : ""}
                    onClick={() => setFilter(f.value)}
                  >
                    {f.label}
                  </button>
                ))}
              </div>

            </div>{/* end tools-header */}

            {loading ? (
              <div className="tools-loading">
                <div className="tools-spinner" />
                <p>Fetching today's tools...</p>
              </div>
            ) : error ? (
              <div className="tools-empty">
                <p>Couldn't connect to the server. Make sure Flask is running on port 5000.</p>
              </div>
            ) : visible.length === 0 ? (
              <div className="tools-empty">
                <p>No tools found{search ? ` for "${search}"` : ""}.</p>
              </div>
            ) : (
              <div className="tools-list">
                {visible.map(tool => <ToolCard key={tool.id} tool={tool} />)}
              </div>
            )}

          </div>
        </main>
      </div>
    </>
  );
}