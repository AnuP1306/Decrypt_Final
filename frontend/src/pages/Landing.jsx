// function Landing() {
//     return <h1>Landing page</h1>;
//   }
  
//   export default Landing;
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/landing.css";

// function Landing() {
  const texts = [
    "it’s giving knowledge",
    "no cap, fr fr 🔥",
    "learn faster than reels",
    "Built Different",
    "Understood the assignment",
  ];

  function Landing() {
    
  // 
  const [currentText, setCurrentText] = useState(0);
const [previousText, setPreviousText] = useState(null);

useEffect(() => {
  const interval = setInterval(() => {

    setPreviousText(currentText);

    setCurrentText(
      (prev) => (prev + 1) % texts.length
    );

    setTimeout(() => {
      setPreviousText(null);
    }, 700);

  }, 3000);

  return () => clearInterval(interval);
}, [currentText]);

  return (
    <>
      {/* NAVBAR */}

      <nav className="landing-nav">
        <div className="nav-inner">

          <div className="nav-left">
            <img
              src="/images/logo.svg"
              alt="Decrypt Logo"
              className="logo"
            />
            <span>DECRYPT</span>
          </div>

          <div className="nav-right">

            <Link
              to="/login"
              className="nav-login"
            >
              Login
            </Link>

            <Link
              to="/signup"
              className="nav-btn"
            >
              Get Started →
            </Link>

          </div>

        </div>
      </nav>

      {/* HERO */}

      <section className="hero">

        <div className="scroll-indicator">
          <span>
            scroll to see what you're missing
          </span>

          <div className="arrow"></div>
        </div>

        <div className="container">

          <div className="badge">
            ⚡ Tech news for people with a
            2-second attention span
          </div>

          <h1 className="hero-title fade-up">
            DECRYPT
          </h1>

          <p className="hero-sub fade-up delay-1">
            Tech news that's{" "}
            <span className="highlight">
              actually
            </span>{" "}
            for you.
          </p>

       <p className="hero-tag">
  <span className="tag-container">

    {previousText !== null && (
      <span className="tag-text exit">
        {texts[previousText]}
      </span>
    )}

    <span
      key={currentText}
      className="tag-text active"
    >
      {texts[currentText]}
    </span>

  </span>
</p>

          <p className="hero-desc fade-up delay-3">
            AI-summarized tech news, tools,
            and student opportunities —
            all in one place.
            No BS. No paywalls.
            Just what matters.
          </p>

          <div className="hero-buttons fade-up delay-4">

            <Link
              to="/signup"
              className="btn-primary"
            >
              Start Decrypting →
            </Link>

            <Link
              to="/home"
              className="btn-secondary"
            >
              Explore Feed →
            </Link>

          </div>

        </div>

        {/* Rings */}

        <div className="ring ring-blue"></div>
        <div className="ring ring-green"></div>

        {/* Dots */}

        <div className="dots">
          <span className="dot dot-1"></span>
          <span className="dot dot-2"></span>
          <span className="dot dot-3"></span>
          <span className="dot dot-4"></span>
          <span className="dot dot-5"></span>
          <span className="dot dot-6"></span>
          <span className="dot dot-7"></span>
          <span className="dot dot-8"></span>
          <span className="dot dot-9"></span>
        </div>

      </section>

      {/* STATS */}

      <section className="stats">

        <div className="stats-grid">

          <div>
            <h2>50+</h2>
            <p>Articles daily</p>
          </div>

          <div>
            <h2>200+</h2>
            <p>AI tools catalogued</p>
          </div>

          <div>
            <h2>30+</h2>
            <p>Student opps listed</p>
          </div>

          <div>
            <h2>3hrs/week</h2>
            <p>Time saved</p>
          </div>

        </div>

      </section>

            {/* FEATURES */}

      <section className="features">

        <div className="features-header">
          <span className="features-badge">
            WHAT'S INSIDE
          </span>

          <h2>
            Features that actually{" "}
            <span className="underline">
              slap
            </span>
          </h2>
        </div>

        <div className="features-grid">

          <div className="feature-card">
            <div className="icon blue">⚡</div>

            <h3>TL;DR News Cards</h3>

            <p>
              Tech news explained like your smart friend
              texted it to you. No more 20-minute reads.
            </p>
          </div>

          <div className="feature-card highlight">
            <div className="icon white">🧠</div>

            <h3>Article ChatBot</h3>

            <p>
              Ask ANYTHING about an article.
              Instant answers without leaving the page.
            </p>
          </div>

          <div className="feature-card">
            <div className="icon green">🛠</div>

            <h3>AI Tools Library</h3>

            <p>
              Lesser-known tools explained simply.
              Free tools prioritized.
            </p>
          </div>

          <div className="feature-card">
            <div className="icon blue">🎓</div>

            <h3>Student Opportunities</h3>

            <p>
              Internships, hackathons, workshops
              and student perks curated for you.
            </p>
          </div>

          <div className="feature-card highlight">
            <div className="icon white">🗂</div>

            <h3>Daily Flashcards</h3>

            <p>
              Learn faster with bite-sized concepts
              delivered every day.
            </p>
          </div>

          <div className="feature-card">
            <div className="icon green">🤖</div>

            <h3>D-Bot Assistant</h3>

            <p>
              Your AI buddy for understanding
              anything in tech.
            </p>
          </div>

        </div>

      </section>

      {/* CTA */}

      <section className="cta">

        <div className="cta-content">

          <h2>
            Ready to <span>DECRYPT</span> the tech world?
          </h2>

          <p>
            Join thousands of Gen Z students who
            actually know what's happening.
          </p>

          <Link
            to="/signup"
            className="cta-btn"
          >
            Create Free Account →
          </Link>

        </div>

        {/* FOOTER */}

        <div className="cta-footer">

          <div className="footer-left">

            <img
              src="/images/logo.svg"
              alt="Decrypt"
              className="logo"
            />

            <span>DECRYPT</span>

          </div>

          <div className="footer-center">
            © 2026 Decrypt. Made for the generation that gets it.
          </div>

          <div className="footer-right">

            <a href="#">
              Privacy
            </a>

            <a href="#">
              Terms
            </a>

            <a href="#">
              Contact
            </a>

          </div>

        </div>

      </section>
    </>
  );
}

export default Landing;