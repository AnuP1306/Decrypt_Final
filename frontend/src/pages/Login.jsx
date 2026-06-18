import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import "../styles/Login.css";


function Login() {
  const navigate = useNavigate();
  const { login, googleLogin, githubLogin } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      setLoading(true);
      await login(email, password);
      navigate("/home");
    } catch (err) {
      if (err.code === "auth/invalid-credential" || err.code === "auth/wrong-password") {
        setError("Wrong email or password. Try again!");
      } else if (err.code === "auth/user-not-found") {
        setError("No account found with this email. Sign up first!");
      } else if (err.code === "auth/too-many-requests") {
        setError("Too many attempts. Please wait a bit and try again.");
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setError("");
    try {
      setLoading(true);
      const { isNewUser } = await googleLogin();
      // New users go to onboarding, returning users go straight to home
      navigate(isNewUser ? "/onboarding-1" : "/home");
    } catch (err) {
      setError("Google sign-in failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGithubLogin = async () => {
    setError("");
    try {
      setLoading(true);
      const { isNewUser } = await githubLogin();
      navigate(isNewUser ? "/onboarding-1" : "/home");
    } catch (err) {
      setError("GitHub sign-in failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      {/* LEFT PANEL */}
      <div className="login-left">
        <div className="login-left-content">
          <img src="/images/logo.svg" alt="Decrypt Logo" className="login-logo" />
          <h1>DECRYPT</h1>
          <p className="tagline">
            "the tech news platform for people who actually want to know what's going on"
          </p>
          <div className="features">
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
              <span>Smart summaries, no fluff</span>
            </div>
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
              <span>AI bot on every article</span>
            </div>
            <div className="feature-item">
              <div className="icon-circle"><img src="/images/thunder.png" alt="icon" /></div>
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
          <a href="/" className="back">← Back to home</a>
          <h2>Welcome back</h2>
          <p className="sub">you were gone? we missed you bestie</p>

          {/* Error box - only shows if there's an error */}
          {error && <div className="error-box">{error}</div>}

          <form className="login-form" onSubmit={handleLogin}>
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
              <a href="/forgot-password">Forgot password?</a>
            </div>
            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? "Logging in..." : "Log In →"}
            </button>
          </form>

          <div className="divider">or continue with</div>
          <div className="socials">
            <button type="button" onClick={handleGoogleLogin} disabled={loading}>
              Google
            </button>
            <button type="button" onClick={handleGithubLogin} disabled={loading}>
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
