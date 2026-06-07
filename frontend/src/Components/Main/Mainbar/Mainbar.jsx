import React from "react";
import "./Mainbar.css";

export default function MainBar() {
  return (
    <section className="mainbar">

      <div className="mainbar__text">
        <h1>Discover Amazing Posts</h1>
        <p>
          Explore articles, tutorials and ideas shared by developers around the world.
        </p>

        <button>Explore Now</button>
      </div>

      <div className="mainbar__images">
        <img
          src="https://source.unsplash.com/500x400/?coding"
          alt="coding"
        />
        <img
          src="https://source.unsplash.com/500x400/?laptop"
          alt="laptop"
        />
      </div>

    </section>
  );
}