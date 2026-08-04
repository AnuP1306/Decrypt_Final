function Navbar({ searchQuery, setSearchQuery }) {
    return (
      <nav className="navbar">
  
        <div className="nav-left">
          <img src="/images/logo.svg" alt="logo" className="logo-img" />
          <p className="logo-text">Decrypt</p>
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
  placeholder="Search news articles"
  value={searchQuery}
  onChange={(e) => setSearchQuery(e.target.value)}
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