import React, { useState } from "react";
import "./Navbar.css";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar__logo">
        <h2>MyBlog</h2>
      </div>

      <div className={`navbar__links ${open ? "active" : ""}`}>
        <a href="/">Home</a>
        <a href="/posts">Posts</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
      </div>

      <div className="navbar__auth">
        <button className="btn login">Login</button>
        <button className="btn register">Register</button>
      </div>

      {/* hamburger */}
      <div className="hamburger" onClick={() => setOpen(!open)}>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </nav>
  );
}