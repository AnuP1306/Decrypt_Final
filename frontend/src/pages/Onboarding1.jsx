import { useState } from "react";
import { useNavigate } from "react-router-dom";


const styles = {
  body: {
    margin: 0,
    background: "#F7F3F0",
    fontFamily: "'Space Grotesk', sans-serif",
  },
  wrapper: {
    width: "100%",
    minHeight: "100vh",
    background: "#F7F3F0",
    fontFamily: "'Space Grotesk', sans-serif",
  },
  topBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "24px 60px 10px",
  },
  logoRow: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  logoImg: {
    width: "42px",
  },
  logoText: {
    fontFamily: "'Syne', sans-serif",
    fontWeight: 750,
    fontSize: "18px",
  },
  progressInfo: {
    fontSize: "14px",
    color: "rgba(0,0,0,0.5)",
  },
  progressBarTrack: {
    height: "6px",
    background: "rgba(0,0,0,0.1)",
    margin: "0 60px",
    borderRadius: "10px",
  },
  progressFill: {
    height: "100%",
    background: "#3F38E8",
    borderRadius: "10px",
    width: "33%",
  },
  content: {
    maxWidth: "820px",
    margin: "60px auto",
    textAlign: "center",
    padding: "0 20px",
  },
  stepPill: {
    display: "inline-flex",
    alignItems: "center",
    gap: "6px",
    background: "rgba(255,140,0,0.12)",
    color: "#FF8C00",
    border: "1.5px solid #FF8C00",
    padding: "8px 16px",
    borderRadius: "22px",
    fontSize: "15px",
    fontWeight: 500,
    marginBottom: "15px",
  },
  h1: {
    fontFamily: "'Syne', sans-serif",
    fontSize: "48px",
    fontWeight: 800,
    lineHeight: 1.2,
    marginBottom: "12px",
    margin: "0 0 12px 0",
  },
  subtitle: {
    color: "rgba(0,0,0,0.5)",
    marginBottom: "40px",
    fontSize: "16px",
  },
  options: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
    marginBottom: "40px",
    width: "100%",
  },
  option: {
    display: "flex",
    alignItems: "center",
    gap: "14px",
    padding: "20px 24px",
    borderRadius: "18px",
    background: "white",
    border: "2px solid rgba(0,0,0,0.08)",
    fontSize: "15px",
    cursor: "pointer",
    transition: "all 0.2s ease",
    textAlign: "left",
    width: "100%",
    boxSizing: "border-box",
  },
  optionActive: {
    background: "linear-gradient(135deg, #4f46e5, #4338ca)",
    color: "#ffffff",
    border: "2px solid transparent",
  },
  optionEmoji: {
    fontSize: "26px",
    flexShrink: 0,
  },
  actions: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  backLink: {
    color: "rgba(0,0,0,0.5)",
    textDecoration: "none",
    fontSize: "15px",
    fontWeight: 500,
    cursor: "pointer",
    transition: "0.2s ease",
    background: "none",
    border: "none",
    padding: 0,
  },
  continueBtn: {
    background: "#A7A4E8",
    opacity: 0.7,
    pointerEvents: "none",
    color: "white",
    border: "none",
    padding: "16px 36px",
    borderRadius: "20px",
    fontFamily: "'Syne', sans-serif",
    fontSize: "18px",
    fontWeight: 800,
    transition: "0.2s ease",
    cursor: "default",
  },
  continueBtnEnabled: {
    opacity: 1,
    background: "linear-gradient(135deg, #4C46E5, #3F38E8)",
    pointerEvents: "auto",
    cursor: "pointer",
    border: "2px solid #30312C",
  },
};

const domainOptions = [
  { emoji: "🤖", label: "Artificial Intelligence", value: "ai" },
  { emoji: "🔌", label: "Electronics", value: "electronics" },
  { emoji: "👨‍💻", label: "Technology", value: "technology" },
];

function Onboarding1() {
  const navigate = useNavigate();
  const [selected, setSelected] = useState(null);
  const [hoveredOption, setHoveredOption] = useState(null);
  const [backHovered, setBackHovered] = useState(false);

  const handleContinue = () => {
    if (!selected) return;
    // ✅ Find the label of the selected option and save it
    const selectedLabel = domainOptions.find((opt) => opt.value === selected)?.label;
    sessionStorage.setItem("onboarding_step1", selectedLabel);
    navigate("/onboarding-2");
  };

  return (
    <div style={styles.wrapper}>
      {/* TOP BAR */}
      <div style={styles.topBar}>
        <div style={styles.logoRow}>
          <img src="/images/logo.svg" alt="Decrypt logo" style={styles.logoImg} />
          <span style={styles.logoText}>DECRYPT</span>
        </div>
        <div style={styles.progressInfo}>1 of 3</div>
      </div>

      {/* PROGRESS BAR */}
      <div style={styles.progressBarTrack}>
        <div style={styles.progressFill} />
      </div>

      {/* CONTENT */}
      <div style={styles.content}>
        <div style={styles.stepPill}>⚡ Step 1</div>

        <h1 style={styles.h1}>What's your vibe?</h1>

        <p style={styles.subtitle}>no judgment, seriously</p>

        <div style={styles.options}>
          {domainOptions.map((opt) => {
            const isActive = selected === opt.value;
            const isHovered = hoveredOption === opt.value;
            return (
              <div
                key={opt.value}
                style={{
                  ...styles.option,
                  ...(isActive ? styles.optionActive : {}),
                  ...(!isActive && isHovered
                    ? { border: "2px solid #3F38E8", transform: "translateY(-2px)" }
                    : {}),
                }}
                onClick={() => setSelected(opt.value)}
                onMouseEnter={() => setHoveredOption(opt.value)}
                onMouseLeave={() => setHoveredOption(null)}
              >
                <span style={styles.optionEmoji}>{opt.emoji}</span>
                <span style={{ color: isActive ? "#fff" : "inherit" }}>{opt.label}</span>
              </div>
            );
          })}
        </div>

        <div style={styles.actions}>
          <button
            style={{
              ...styles.backLink,
              ...(backHovered ? { color: "#000" } : {}),
            }}
            onClick={() => navigate(-1)}
            onMouseEnter={() => setBackHovered(true)}
            onMouseLeave={() => setBackHovered(false)}
          >
            ← back
          </button>

          <button
            style={{
              ...styles.continueBtn,
              ...(selected ? styles.continueBtnEnabled : {}),
            }}
            onClick={handleContinue}
            disabled={!selected}
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );
}

export default Onboarding1;