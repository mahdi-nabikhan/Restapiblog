import React from "react";
import "./SideBar.css";
import { Link } from "react-router-dom";

export default function SideBar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__logo">
        <h2>MyPanel</h2>
      </div>

      <nav className="sidebar__menu">
        <Link to="/panel" className="sidebar__link">Dashboard</Link>
        <Link to="/panel/profile" className="sidebar__link">Profile</Link>
        <Link to="/panel/posts" className="sidebar__link">My Posts</Link>
        <Link to="/panel/settings" className="sidebar__link">Settings</Link>
      </nav>

      <div className="sidebar__footer">
        <button className="logout">Logout</button>
      </div>
    </aside>
  );
}