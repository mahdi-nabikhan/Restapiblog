import React, { useEffect, useState } from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";

export default function Navbar() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);

  const getUser = async () => {
    try {
      const res = await fetch("http://localhost:8000/accounts/api/v1/me/", {
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

  const logout = async () => {
    try {
      await fetch("http://localhost:8000/accounts/api/v1/logout/", {
        method: "POST",
        credentials: "include",
      });

      setUser(null);
    } catch (err) {
      console.log(err);
    }
  };

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
        <Link to={''}>Home</Link>
        <Link to = {'add/post'}>Add Posts</Link>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
      </div>

      {/* AUTH AREA */}
      <div className="navbar__auth">
        {user ? (
          <div className="navbar__user">
            <span className="navbar__email">{user.email}</span>
            <button className="btn logout" onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <div className="navbar__buttons LinkText">
            <Link to={'login'} className="btn login">Login</Link>
            <Link to= {'register'} className="btn register">Register</Link>
          </div>
        )}
      </div>

      {/* HAMBURGER */}
      <div className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </nav>
  );
}