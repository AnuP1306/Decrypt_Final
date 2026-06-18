import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import "../styles/Signup.css";

function Signup() {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    if (!name.trim()) return setError("Please enter your name");
    if (!email.trim()) return setError("Please enter your email");
    if (!password.trim()) return setError("Please enter a password");
    if (password.length < 6) return setError("Password must be at least 6 characters");
    if (password !== confirmPassword) return setError("Passwords do not match");
    if (!acceptedTerms) return setError("Please accept the Terms & Conditions");

    try {
      setLoading(true);
      await signup(name, email, password); // creates Firebase user + Firestore doc
      navigate("/onboarding-1");
    } catch (err) {
      // Firebase gives readable error messages
      if (err.code === "auth/email-already-in-use") {
        setError("This email is already registered. Try logging in!");
      } else if (err.code === "auth/invalid-email") {
        setError("Invalid email address.");
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-wrapper">
      {/* LEFT SIDE */}
      <div className="signup-left">
        <a href="/" className="back">← Back</a>

        <div className="signup-container">
          <div className="logo-row">
            <img src="/images/logo.svg" alt="Decrypt Logo" />
            <span className="logo-text">DECRYPT</span>
          </div>

          <h1>Join the gang</h1>
          <p className="subtitle">
            free, no credit card, no weird emails. just vibes and news.
          </p>

          {/* Error box - only shows if there's an error */}
          {error && <div className="error-box">{error}</div>}

          <form className="signup-form" onSubmit={handleSignup}>
            <div className="form-group">
              <label>What do we call you?</label>
              <input
                type="text"
                placeholder="Your name (or alias, we don't judge)"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Your email (we won't spam, promise)</label>
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
                placeholder="don't mess this up"
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
                <a href="/">Privacy Policy</a>. I'm not a robot (hopefully).
              </span>
            </div>

            <button className="signup-btn" type="submit" disabled={loading}>
              {loading ? "Creating account..." : "Create Account →"}
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
          <img src="/images/Technewz.png" alt="Technewz" className="Technewz-img" />
          <p className="right-tag">Built for the Locked-in generation</p>
          <div className="features">
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
              <span>50+ news articles daily</span>
            </div>
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
              <span>AI tools for students</span>
            </div>
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
              <span>Free student opportunities</span>
            </div>
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
              <span>10-min daily flashcards</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Signup;
