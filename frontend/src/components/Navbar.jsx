function Navbar() {
    return (
      <nav className="navbar">
  
        <div className="nav-left">
          <img src="/images/logo.svg" alt="logo" className="logo-img" />
          <h1 className="logo-text">Decrypt</h1>
        </div>
  
        <div className="nav-center">
          <div className="search-wrapper">
            <img
              src="/images/search.png"
              className="search-icon"
              alt=""
            />
  
            <input
              type="text"
              placeholder="Search topics, tools, news..."
              className="search-input"
            />
          </div>
        </div>
  
        <div className="nav-right">
          <div className="notif-wrapper">
            <img
              src="/images/notification.png"
              className="notif-icon"
              alt=""
            />
          </div>
        </div>
  
      </nav>
    );
  }
  
  export default Navbar;