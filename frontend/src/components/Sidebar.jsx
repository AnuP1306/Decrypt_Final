import { Link, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../firebase";

function Sidebar() {

  const { currentUser, logout } = useAuth();

const [user, setUser] = useState({
  name: "Explorer",
  domain: "AI",
  level: "Beginner"
});

  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] =
    useState(false);

    useEffect(() => {
      async function loadUser() {
        // if (!currentUser) return;
        if (!currentUser) {
          setUser({
            name: "Explorer",
            domain: "AI",
            level: "Beginner",
          });
          return;
        }
    
        const userRef = doc(db, "users", currentUser.uid);
        const snap = await getDoc(userRef);
    
        if (snap.exists()) {
          const data = snap.data();
    
          setUser({
            name: data.name || "Explorer",
            domain: data.personalization?.vibe || "AI",
            level:
              data.personalization?.knowledgeLevel?.split("—")[0]?.trim() ||
              "Beginner"
          });
        }
      }
    
      loadUser();
    }, [currentUser]);

    async function handleLogout() {
      try {
        await logout();
    
        // Optional: remove any user-specific localStorage
        localStorage.removeItem("userLevel");
    
        navigate("/");
      } catch (err) {
        console.error("Logout failed:", err);
      }
    }

  return (
    <div
    className={`sidebar ${
      collapsed
        ? "collapsed"
        : ""
    }`}
    id="sidebar"
  >

      <div className="sidebar-top">

        <div className="user-info">

        <div className="user-avatar">
  {user.name[0].toUpperCase()}
</div>

          <div className="user-text">
            <p className="user-name">{user.name}</p>
            <span className="user-role">
            {user.domain} · {user.level}
            </span>
          </div>

          <button
  className="menu-toggle"
  onClick={() =>
    setCollapsed(!collapsed)
  }
>
            <img src="/images/menu.png" alt="" />
          </button>

        </div>

      </div>

      <div className="sidebar-menu">

        <Link
          to="/home"
          className={`menu-item ${
            location.pathname === "/home" ? "active" : ""
          }`}
        >
          <img src="/images/home.png" alt="" />
          <span>Home Feed</span>
        </Link>

        <Link
          to="/daily-brief"
          className={`menu-item ${
            location.pathname === "/daily-brief" ? "active" : ""
          }`}
        >
          <img src="/images/bolt.png" alt="" />
          <span>Daily Brief</span>
        </Link>

        <Link
          to="/tools"
          className={`menu-item ${
            location.pathname === "/tools" ? "active" : ""
          }`}
        >
          <img src="/images/tools-1.png" alt="" />
          <span>Tools Library</span>
        </Link>

        <Link
          to="/opportunities"
          className={`menu-item ${
            location.pathname === "/opportunities" ? "active" : ""
          }`}
        >
          <img src="/images/opportunity.png" alt="" />
          <span>Student Opportunities</span>
        </Link>

        <Link
          to="/saved"
          className={`menu-item ${
            location.pathname === "/saved" ? "active" : ""
          }`}
        >
          <img src="/images/saved.png" alt="" />
          <span>Saved Items</span>
        </Link>

      </div>

      <div className="sidebar-bottom">

        <div className="menu-item">
          <img src="/images/bell.png" alt="" />
          <span>Notifications</span>
        </div>

        <div className="menu-item">
          <img src="/images/settings.png" alt="" />
          <span>Settings</span>
        </div>

        <button
  className="menu-item logout"
  onClick={handleLogout}
>
  <img src="/images/logout.png" alt="" />
  <span>Log Out</span>
</button>

      </div>

    </div>
  );
}

export default Sidebar;