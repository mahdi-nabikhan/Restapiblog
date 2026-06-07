import React from "react";
import "./Profile.css";

export default function Profile() {
  return (
    <div className="profile-container">
      <div className="profile-card">

        <div className="profile-header">
          <img
            className="profile-avatar"
            src="https://i.pravatar.cc/150?img=12"
            alt="avatar"
          />

          <div className="profile-info">
            <h2>John Doe</h2>
            <p>johndoe@gmail.com</p>
          </div>
        </div>

        <div className="profile-body">
          <div className="profile-item">
            <span>Username</span>
            <p>john_doe</p>
          </div>

          <div className="profile-item">
            <span>Joined</span>
            <p>2026 / 01 / 10</p>
          </div>

          <div className="profile-item">
            <span>Role</span>
            <p>User</p>
          </div>
        </div>

        <div className="profile-actions">
          <button className="btn edit">Edit Profile</button>
          <button className="btn logout">Logout</button>
        </div>

      </div>
    </div>
  );
}