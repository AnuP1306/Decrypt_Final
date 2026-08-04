import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

// Pages
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

import Onboarding1 from "./pages/Onboarding1";
import Onboarding2 from "./pages/Onboarding2";
import Onboarding3 from "./pages/Onboarding3";

import Home from "./pages/Home";
import DailyBrief from "./pages/DailyBrief";
import Tools from "./pages/Tools";
import Opportunities from "./pages/Opportunities";
import Saved from "./pages/Saved";

// Auth
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    // AuthProvider MUST wrap BrowserRouter so every page/component
    // in the whole app can access currentUser, login, logout etc.
    <AuthProvider>
      <BrowserRouter>
        <Routes>

          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Onboarding - auth required (user just signed up) but
              onboardingCompleted check is skipped here intentionally */}
          <Route path="/onboarding-1" element={<Onboarding1 />} />
          <Route path="/onboarding-2" element={<Onboarding2 />} />
          <Route path="/onboarding-3" element={<Onboarding3 />} />

          {/* Protected Routes */}
          <Route path="/home" element={<Home />} />
          <Route path="/daily-brief" element={<DailyBrief />} />
          <Route path="/tools" element={<Tools />} />
          <Route path="/opportunities" element={<Opportunities />} />
          <Route path="/saved" element={<ProtectedRoute><Saved /></ProtectedRoute>} />

        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
