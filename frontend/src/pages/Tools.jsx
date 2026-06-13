import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import "../styles/tools.css";

const tools = [
  // ── Research ────────────────────────────────────────────────────────────
  {
    id: 1,
    name: "Elicit",
    description: "AI research assistant that finds and summarizes academic papers. Much easier than traditional research tools.",
    category: "research",
    rating: "4.8",
    price: "FREE",
    tags: ["#Research", "#AI", "#Papers"],
    url: "https://elicit.com",
    image: "/images/elicit api.jpeg",
  },
  {
    id: 2,
    name: "Scite",
    description: "Shows whether research papers are supported or contradicted by other studies.",
    category: "research",
    rating: "4.6",
    price: "FREE",
    tags: ["#Citations", "#Research", "#AI"],
    url: "https://scite.ai",
    image: "/images/scite.ai.jpeg",
  },
  {
    id: 3,
    name: "Consensus",
    description: "Answers questions using only scientific studies and research-backed evidence.",
    category: "research",
    rating: "4.7",
    price: "FREE",
    tags: ["#Science", "#Research", "#Facts"],
    url: "https://consensus.app",
    image: "/images/consensus.jpeg",
  },

  // ── Design ──────────────────────────────────────────────────────────────
  {
    id: 4,
    name: "Visily",
    description: "AI UI design tool that converts text into app screens. Beginner-friendly alternative to Figma.",
    category: "design",
    rating: "4.9",
    price: "FREE",
    tags: ["#UI", "#Design", "#AI"],
    url: "https://visily.ai",
    image: "/images/visily.jpeg",
  },
  {
    id: 5,
    name: "Uizard",
    description: "Transforms sketches into real app designs instantly using AI.",
    category: "design",
    rating: "4.9",
    price: "FREE",
    tags: ["#Prototype", "#Design", "#AI"],
    url: "https://uizard.io",
    image: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
  },
  {
    id: 6,
    name: "Shots.so",
    description: "Create stunning mockups instantly for your UI screenshots and portfolios.",
    category: "design",
    rating: "4.9",
    price: "FREE",
    tags: ["#Design", "#Mockup", "#UI"],
    url: "https://shots.so",
    image: "https://cdn-icons-png.flaticon.com/512/1006/1006771.png",
  },

  // ── Coding ──────────────────────────────────────────────────────────────
  {
    id: 7,
    name: "Codeium",
    description: "Free AI coding assistant similar to GitHub Copilot with powerful autocomplete.",
    category: "coding",
    rating: "4.9",
    price: "FREE",
    tags: ["#Coding", "#AI", "#Dev"],
    url: "https://codeium.com",
    image: "https://cdn-icons-png.flaticon.com/512/5968/5968350.png",
  },
  {
    id: 8,
    name: "Mutable AI",
    description: "AI that edits, improves and explains your code directly inside your editor.",
    category: "coding",
    rating: "4.9",
    price: "FREE",
    tags: ["#Code", "#AI", "#Productivity"],
    url: "https://mutable.ai",
    image: "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
  },
  {
    id: 9,
    name: "Pieces",
    description: "Automatically saves useful code snippets so you never lose important code again.",
    category: "coding",
    rating: "4.9",
    price: "FREE",
    tags: ["#Snippets", "#Dev", "#Tools"],
    url: "https://pieces.app",
    image: "https://cdn-icons-png.flaticon.com/512/906/906334.png",
  },

  // ── Visualization ───────────────────────────────────────────────────────
  {
    id: 10,
    name: "Flourish",
    description: "Create interactive charts and storytelling dashboards easily.",
    category: "visualization",
    rating: "4.9",
    price: "FREE",
    tags: ["#Data", "#Charts", "#Visualization"],
    url: "https://flourish.studio",
    image: "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
  },
  {
    id: 11,
    name: "RAWGraphs",
    description: "Advanced open-source tool for creating unique and complex data visualizations.",
    category: "visualization",
    rating: "4.9",
    price: "FREE",
    tags: ["#Graphs", "#Data", "#OpenSource"],
    url: "https://rawgraphs.io",
    image: "https://cdn-icons-png.flaticon.com/512/2920/2920349.png",
  },
  {
    id: 12,
    name: "ChartAI",
    description: "Generate charts instantly by simply describing your data in text.",
    category: "visualization",
    rating: "4.9",
    price: "FREE",
    tags: ["#AI", "#Charts", "#Data"],
    url: "#",
    image: "https://cdn-icons-png.flaticon.com/512/2721/2721273.png",
  },

  // ── Audio ───────────────────────────────────────────────────────────────
  {
    id: 13,
    name: "Adobe Podcast AI",
    description: "Enhance your voice to studio-quality audio using AI.",
    category: "audio",
    rating: "4.9",
    price: "FREE",
    tags: ["#Audio", "#AI", "#Podcast"],
    url: "https://podcast.adobe.com",
    image: "https://cdn-icons-png.flaticon.com/512/5968/5968520.png",
  },
  {
    id: 14,
    name: "Krisp",
    description: "Removes background noise from calls and recordings in real time.",
    category: "audio",
    rating: "4.9",
    price: "FREE",
    tags: ["#Audio", "#NoiseCancel", "#Meetings"],
    url: "https://krisp.ai",
    image: "https://cdn-icons-png.flaticon.com/512/727/727269.png",
  },
  {
    id: 15,
    name: "Auphonic",
    description: "Automatically balances audio levels for professional-quality sound.",
    category: "audio",
    rating: "4.9",
    price: "FREE",
    tags: ["#Audio", "#Editing", "#Podcast"],
    url: "https://auphonic.com",
    image: "https://cdn-icons-png.flaticon.com/512/727/727245.png",
  },

  // ── Presentation ────────────────────────────────────────────────────────
  {
    id: 16,
    name: "Gamma",
    description: "Create beautiful AI-powered presentations faster than PowerPoint.",
    category: "presentation",
    rating: "4.9",
    price: "FREE",
    tags: ["#Presentation", "#AI", "#Slides"],
    url: "https://gamma.app",
    image: "https://cdn-icons-png.flaticon.com/512/1828/1828919.png",
  },
  {
    id: 17,
    name: "Tome",
    description: "Story-based AI presentation tool focused on narrative storytelling.",
    category: "presentation",
    rating: "4.9",
    price: "FREE",
    tags: ["#Storytelling", "#Slides", "#AI"],
    url: "https://tome.app",
    image: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
  },
  {
    id: 18,
    name: "Decktopus",
    description: "Auto-generates complete presentations with design and content.",
    category: "presentation",
    rating: "4.9",
    price: "FREE",
    tags: ["#Slides", "#AI", "#Productivity"],
    url: "https://decktopus.com",
    image: "https://cdn-icons-png.flaticon.com/512/1828/1828817.png",
  },
];

const FILTERS = [
  { label: "All",            value: "all"           },
  { label: "Research",       value: "research"      },
  { label: "Visualization",  value: "visualization" },
  { label: "Audio",          value: "audio"         },
  { label: "Presentation",   value: "presentation"  },
  { label: "Design",         value: "design"        },
  { label: "Coding",         value: "coding"        },
];

function Tools() {
  const navigate = useNavigate();
  const [currentFilter, setCurrentFilter] = useState("all");
  const [searchQuery, setSearchQuery]     = useState("");

  const filtered = tools.filter(tool => {
    const matchesFilter =
      currentFilter === "all" || tool.category === currentFilter;

    const q = searchQuery.toLowerCase();
    const matchesSearch =
      tool.name.toLowerCase().includes(q) ||
      tool.description.toLowerCase().includes(q);

    return matchesFilter && matchesSearch;
  });

  return (
    <>
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main className="main-content">
          <div className="tools-page">

            {/* Back button */}
            <button className="back-btn" onClick={() => navigate("/home")}>
              ← Back
            </button>

            {/* Top label */}
           <div className="opp-mini-header">
              <div className="tools-icon-box">
                <img src="/images/wrench.png" alt="tool" />
              </div>
              <span className="opp-mini-text">TOOLS LIBRARY</span>
            </div>

            {/* Heading */}
            <h1 className="page-title">
              AI tools that actually{" "}
              <span className="heighlight">go hard</span>
            </h1>
            <p className="page-subtitle">
              The lesser-known, criminally underrated AI tools and sites. Free stuff
              prioritized. Your LinkedIn bio is about to level up.
            </p>

            {/* Stats */}
            <div className="stats">
              <div className="card2">
                <h2>200+</h2>
                <p>Tools Listed</p>
              </div>
              <div className="card2">
                <h2>80%</h2>
                <p>Free Tools</p>
              </div>
              <div className="card2">
                <h2>Weekly</h2>
                <p>Updated</p>
              </div>
            </div>

            {/* Search */}
            <div className="search-box">
              <input
                type="text"
                placeholder="Search tools..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
            </div>

            {/* Filter buttons */}
            <div className="categories">
              {FILTERS.map(f => (
                <button
                  key={f.value}
                  data-filter={f.value}
                  className={currentFilter === f.value ? "active" : ""}
                  onClick={() => setCurrentFilter(f.value)}
                >
                  {f.label}
                </button>
              ))}
            </div>

            {/* Tool cards */}
            <div className="tools-list">
              {filtered.map(tool => (
                <div key={tool.id} className="card" data-category={tool.category}>

                  <div className="card-img">
                    <img src={tool.image} alt={tool.name} />
                    <div className="rating">⭐ {tool.rating}</div>
                    <div className="tags-top">
                      <span className="tag free">{tool.price}</span>
                      <span className="tag category">{tool.category}</span>
                    </div>
                  </div>

                  <div className="card-body">
                    <h3>{tool.name}</h3>
                    <p>{tool.description}</p>
                    <div className="hashtags">
                      {tool.tags.map(tag => (
                        <span key={tag}>{tag}</span>
                      ))}
                    </div>
                    <a href={tool.url} target="_blank" rel="noreferrer" className="btn">
                      Check it out ↗
                    </a>
                  </div>

                </div>
              ))}
            </div>

          </div>
        </main>
      </div>
    </>
  );
}

export default Tools;
