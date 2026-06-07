import React from "react";
import "./PostList.css";

export default function PostList() {
  return (
    <div className="posts-container">
      <h2 className="posts-title">Latest Posts</h2>

      <div className="posts-grid">
        <div className="post-card">
          <h3>Post Title 1</h3>
          <p>
            This is a short description for the first post. It shows preview text.
          </p>
        </div>

        <div className="post-card">
          <h3>Post Title 2</h3>
          <p>
            This is a short description for the second post. It shows preview text.
          </p>
        </div>

        <div className="post-card">
          <h3>Post Title 3</h3>
          <p>
            This is a short description for the third post. It shows preview text.
          </p>
        </div>
      </div>
    </div>
  );
}