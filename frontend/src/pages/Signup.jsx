import { useState } from "react";
import "../styles/Signup.css";

import logo from "../assets/images/logo.svg";
import thunder from "../assets/images/thunder.png";
import technewz from "../assets/images/Technewz.png";

function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [acceptedTerms, setAcceptedTerms] = useState(false);

  const handleSignup = (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    console.log({
      name,
      email,
      password,
      acceptedTerms,
    });

    // Firebase signup code will be added later
  };

  return (
    <div className="signup-wrapper">
      {/* LEFT SIDE */}
      <div className="signup-left">
        <a href="/" className="back">
          ← Back
        </a>

        <div className="signup-container">
          <div className="logo-row">
            <img src={logo} alt="Decrypt Logo" />
            <span className="logo-text">DECRYPT</span>
          </div>

          <h1>Join the gang</h1>

          <p className="subtitle">
            free, no credit card, no weird emails. just vibes and news.
          </p>

          <form className="signup-form" onSubmit={handleSignup}>
            <div className="form-group">
              <label>What do we call you?</label>
              <input
                type="text"
                placeholder="Your name (or alias, we don’t judge)"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Your email (we won’t spam, promise)</label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                placeholder="make it good"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                placeholder="don’t mess this up"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>

            <div className="terms">
              <input
                type="checkbox"
                checked={acceptedTerms}
                onChange={(e) => setAcceptedTerms(e.target.checked)}
              />

              <span>
                I agree to the <a href="/">Terms of Service</a> and{" "}
                <a href="/">Privacy Policy</a>. I’m not a robot (hopefully).
              </span>
            </div>

            <button className="signup-btn" type="submit">
              Create Account →
            </button>
          </form>

          <p className="login-link">
            Already a Decrypter? <a href="/login">Log in</a>
          </p>
        </div>
      </div>

      {/* RIGHT SIDE */}
      <div className="signup-right">
        <div className="right-content">
          <img
            src={technewz}
            alt="Technewz"
            className="Technewz-img"
          />

          <p className="right-tag">
            Built for the Locked-in generation
          </p>

          <div className="features">
            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>50+ news articles daily</span>
            </div>

            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>AI tools for students</span>
            </div>

            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>Free student opportunities</span>
            </div>

            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>10-min daily flashcards</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Signup;