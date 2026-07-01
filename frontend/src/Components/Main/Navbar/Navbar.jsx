import React, { useEffect, useState } from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";
import BACKEND_URL from "../../../Utils";

export default function Navbar() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const [menuOpen, setMenuOpen] = useState(false);

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);


  const getUser = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/accounts/api/v1/me/`, {
        method: "GET",
        credentials: "include",
      });

      if (!res.ok) {
        setUser(null);
        return;
      }

      const data = await res.json();
      setUser(data);
    } catch (err) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getUser();
  }, []);

  // ======================
  // LOGOUT
  // ======================
  const logout = async () => {
    try {
      await fetch(`${BACKEND_URL}/accounts/api/v1/jwt/custom/delete/`, {
        method: "POST",
        credentials: "include",
      });

      setUser(null);
    } catch (err) {
      console.log(err);
    }
  };

  // ======================
  // SEARCH
  // ======================
  const handleSearch = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length < 2) {
      setResults([]);
      return;
    }

    try {
      setSearchLoading(true);

      const res = await fetch(
        `${BACKEND_URL}/blog/api/v1/search/?q=${value}`,
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (!res.ok) throw new Error("Search failed");

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.log(err);
      setResults([]);
    } finally {
      setSearchLoading(false);
    }
  };

  // ======================
  // LOADING UI
  // ======================
  if (loading) {
    return (
      <div className="navbar">
        <div className="navbar__logo">MyBlog</div>
        <div className="navbar__loading">Loading...</div>
      </div>
    );
  }

  return (
    <nav className="navbar">

      {/* LOGO */}
      <div className="navbar__logo">
        <h2>MyBlog</h2>
      </div>

      {/* LINKS */}
      <div className={`navbar__links ${menuOpen ? "active" : ""}`}>
        <Link to="/">Home</Link>
        <Link to="/add/post">Add Posts</Link>
        <Link to="/about/us">About Us</Link>
        <Link to="/contact/us">Contact Us</Link>
      </div>

      {/* SEARCH */}
      <div className="navbar__search">

        <input
          type="text"
          placeholder="Search posts..."
          value={query}
          onChange={handleSearch}
          onFocus={() => setSearchOpen(true)}
        />

        {searchOpen && (
          <div className="search-modal">

            {searchLoading && (
              <p className="search-message">Searching...</p>
            )}

            {!searchLoading &&
              results.length === 0 &&
              query.length > 1 && (
                <p className="search-message">
                  No results found
                </p>
              )}

            {results.map((post) => (
              <Link
                key={post.id}
                to={`/post/${post.id}`}
                className="search-item"
                onClick={() => {
                  setSearchOpen(false);
                  setQuery("");
                  setResults([]);
                }}
              >
                <h4>{post.title}</h4>
                <p>{post.snippet}</p>
              </Link>
            ))}

          </div>
        )}
      </div>

      {/* AUTH */}
      <div className="navbar__auth">

        {user ? (
          <div className="navbar__user">
            <span className="navbar__email">
              {user.email}
            </span>

            <button className="btn logout" onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <div className="navbar__buttons">
            <Link to="/login" className="btn login">
              Login
            </Link>
            <Link to="/register" className="btn register">
              Register
            </Link>
          </div>
        )}

      </div>

      {/* HAMBURGER */}
      <div
        className="hamburger"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        <span></span>
        <span></span>
        <span></span>
      </div>

    </nav>
  );
}