import React from "react";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">

        {/* About */}
        <div className="footer-section">
          <h3>About</h3>
          <p>
            A modern blog platform built with Django REST Framework and React.
            Clean, fast and scalable architecture.
          </p>
        </div>

        {/* Links */}
        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li>Home</li>
            <li>Posts</li>
            <li>Login</li>
            <li>Register</li>
          </ul>
        </div>

        {/* Contact */}
        <div className="footer-section">
          <h3>Contact</h3>
          <p>Email: support@blog.com</p>
          <p>Phone: +00 123 456 789</p>
          <p>Location: Remote</p>
        </div>

      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} MyBlog. All rights reserved.</p>
      </div>
    </footer>
  );
}