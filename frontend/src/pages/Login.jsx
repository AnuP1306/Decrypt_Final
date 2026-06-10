import { useState } from "react";
import "../styles/Login.css";

import logo from "../assets/images/logo.svg";
import thunder from "../assets/images/thunder.png";
function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    console.log("Login:", {
      email,
      password,
    });

    // Firebase login code will be added later
  };

  const googleLogin = () => {
    console.log("Google Login");
  };

  const githubLogin = () => {
    console.log("GitHub Login");
  };

  return (
    <div className="login-wrapper">
      {/* LEFT PANEL */}
      <div className="login-left">
        <div className="login-left-content">
          <img src={logo} alt="Decrypt Logo" className="login-logo" />

          <h1>DECRYPT</h1>

          <p className="tagline">
            "the tech news platform for people who actually want to know what’s
            going on"
          </p>

          <div className="features">
            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>Smart summaries, no fluff</span>
            </div>

            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>AI bot on every article</span>
            </div>

            <div className="feature-item">
              <div className="icon-circle">
                <img src={thunder} alt="icon" />
              </div>
              <span>Student perks unlocked</span>
            </div>
          </div>

          <div className="login-rings">
            <div className="ring ring-blue"></div>
            <div className="ring ring-green"></div>
          </div>
        </div>
      </div>

      {/* RIGHT PANEL */}
      <div className="login-right">
        <div className="login-box">
          <a href="/" className="back">
            ← Back to home
          </a>

          <h2>Welcome back</h2>

          <p className="sub">
            you were gone? we missed you bestie
          </p>

          <form onSubmit={handleLogin}>
            <label>Email</label>

            <input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <label>Password</label>

            <input
              type="password"
              placeholder="your secret stuff"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <div className="forgot">
              <a href="/">Forgot password?</a>
            </div>

            <button type="submit" className="login-btn">
              Log In →
            </button>
          </form>

          <div className="divider">or continue with</div>

          <div className="socials">
            <button type="button" onClick={googleLogin}>
              Google
            </button>

            <button type="button" onClick={githubLogin}>
              GitHub
            </button>
          </div>

          <p className="signup">
            New here? <a href="/signup">Create an account</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;