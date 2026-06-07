import React from "react";
import "./TopBar.css";

export default function TopBar() {
  return (
    <header className="topbar">
      <div className="topbar__left">
        <h3>Dashboard</h3>
      </div>

      <div className="topbar__right">
        <div className="topbar__search">
          <input type="text" placeholder="Search..." />
        </div>

        <div className="topbar__user">
          <img
            src="https://i.pravatar.cc/40"
            alt="user"
          />
          <span>John Doe</span>
        </div>
      </div>
    </header>
  );
}