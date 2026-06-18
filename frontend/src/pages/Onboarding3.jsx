import { saveOnboarding } from "../utils/saveOnboarding";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const styles = {
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
    width: "100%",
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
    margin: "0 0 12px 0",
  },
  subtitle: {
    color: "rgba(0,0,0,0.5)",
    marginBottom: "40px",
    fontSize: "16px",
  },
  options: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "18px",
    marginBottom: "40px",
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
    boxSizing: "border-box",
  },
  optionActive: {
    background: "linear-gradient(135deg, #4C46E5, #3F38E8)",
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
    fontSize: "15px",
    fontWeight: 500,
    cursor: "pointer",
    transition: "0.2s ease",
    background: "none",
    border: "none",
    padding: 0,
    fontFamily: "'Space Grotesk', sans-serif",
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
  errorText: {
    color: "#cc0000",
    fontSize: "14px",
    marginBottom: "12px",
  },
};

const topicOptions = [
  { emoji: "🤖", label: "Machine Learning", value: "ml" },
  { emoji: "⌨️", label: "Web Dev", value: "webdev" },
  { emoji: "🦾", label: "Robotics", value: "robotics" },
  { emoji: "☁️", label: "Cloud Computing", value: "cloud" },
  { emoji: "⚛️", label: "Quantum Computing", value: "quantum" },
  { emoji: "🛰️", label: "Space Technology", value: "space" },
  { emoji: "🛜", label: "IOT", value: "iot" },
  { emoji: "🔐", label: "Cybersecurity", value: "cybersecurity" },
];

function Onboarding3() {
  const navigate = useNavigate();
  const { currentUser } = useAuth(); // ← gets the logged-in user

  const [selected, setSelected] = useState(new Set());
  const [hoveredOption, setHoveredOption] = useState(null);
  const [backHovered, setBackHovered] = useState(false);
  const [btnHovered, setBtnHovered] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const toggleOption = (value) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(value)) {
        next.delete(value);
      } else {
        next.add(value);
      }
      return next;
    });
  };

  const handleContinue = async () => {
    if (selected.size === 0) return;
    setError("");
    setLoading(true);

    // Get step 1 and step 2 answers saved by your teammates in sessionStorage
    const vibe = sessionStorage.getItem("onboarding_step1") || "";
    const knowledgeLevel = sessionStorage.getItem("onboarding_step2") || "";

    // Step 3: convert selected Set → array of labels e.g. ["Machine Learning", "Cloud Computing"]
    const interests = topicOptions
      .filter((opt) => selected.has(opt.value))
      .map((opt) => opt.label);

    try {
      // ✅ This saves everything to Firestore under users/{uid}/personalization
      await saveOnboarding(currentUser.uid, {
        vibe,
        knowledgeLevel,
        interests,
      });

      // Clear session storage since we're done with onboarding
      sessionStorage.clear();

      navigate("/home");
    } catch (err) {
      console.error("Save failed:", err);
      setError("Something went wrong saving your preferences. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const isEnabled = selected.size > 0;

  return (
    <div style={styles.wrapper}>
      {/* TOP BAR */}
      <div style={styles.topBar}>
        <div style={styles.logoRow}>
          <img src="/images/logo.svg" alt="Decrypt logo" style={styles.logoImg} />
          <span style={styles.logoText}>DECRYPT</span>
        </div>
        <div style={styles.progressInfo}>3 of 3</div>
      </div>

      {/* PROGRESS BAR */}
      <div style={styles.progressBarTrack}>
        <div style={styles.progressFill} />
      </div>

      {/* CONTENT */}
      <div style={styles.content}>
        <div style={styles.stepPill}>⚡ Step 3</div>

        <h1 style={styles.h1}>
          what topics do you<br />want more of?
        </h1>

        <p style={styles.subtitle}>
          your feed will be based on this (pick as many as you want)
        </p>

        {/* OPTIONS — 2-column grid, multi-select */}
        <div style={styles.options}>
          {topicOptions.map((opt) => {
            const isActive = selected.has(opt.value);
            const isHovered = hoveredOption === opt.value;
            return (
              <div
                key={opt.value}
                style={{
                  ...styles.option,
                  ...(isActive ? styles.optionActive : {}),
                  ...(!isActive && isHovered
                    ? { borderColor: "#3F38E8", transform: "translateY(-2px)" }
                    : {}),
                }}
                onClick={() => toggleOption(opt.value)}
                onMouseEnter={() => setHoveredOption(opt.value)}
                onMouseLeave={() => setHoveredOption(null)}
              >
                <span style={styles.optionEmoji}>{opt.emoji}</span>
                <span style={{ color: isActive ? "#fff" : "inherit" }}>{opt.label}</span>
              </div>
            );
          })}
        </div>

        {/* Error message */}
        {error && <p style={styles.errorText}>{error}</p>}

        {/* ACTIONS */}
        <div style={styles.actions}>
          <button
            style={{
              ...styles.backLink,
              ...(backHovered ? { color: "#000" } : {}),
            }}
            onClick={() => navigate("/onboarding-2")}
            onMouseEnter={() => setBackHovered(true)}
            onMouseLeave={() => setBackHovered(false)}
          >
            ← back
          </button>

          <button
            style={{
              ...styles.continueBtn,
              ...(isEnabled ? styles.continueBtnEnabled : {}),
              ...(isEnabled && btnHovered
                ? { transform: "translateY(-2px)", boxShadow: "4px 4px 0px #30312C" }
                : {}),
            }}
            onClick={handleContinue}
            disabled={!isEnabled || loading}
            onMouseEnter={() => setBtnHovered(true)}
            onMouseLeave={() => setBtnHovered(false)}
          >
            {loading ? "Saving..." : "Let's go! →"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Onboarding3;
