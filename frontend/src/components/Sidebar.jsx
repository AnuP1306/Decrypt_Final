import { Link, useLocation } from "react-router-dom";

function Sidebar() {

  const location = useLocation();

  return (
    <div className="sidebar" id="sidebar">

      <div className="sidebar-top">

        <div className="user-info">

          <div className="user-avatar">E</div>

          <div className="user-text">
            <p className="user-name">Explorer</p>
            <span className="user-role">
              AI · Beginner
            </span>
          </div>

          <button className="menu-toggle">
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

        <Link to="/" className="menu-item logout">
          <img src="/images/logout.png" alt="" />
          <span>Log Out</span>
        </Link>

      </div>

    </div>
  );
}

export default Sidebar;