import React from "react";
import "./Mainbar.css";
import Typewriter from 'typewriter-effect'

export default function MainBar() {
  return (
    <section className="mainbar">

      <div className="mainbar__text">
        <h1>Discover Amazing Posts</h1>
        <Typewriter options={{
          autoStart: true,
          loop: true,
          delay: 50,
          deleteSpeed: 30,
        }} onInit={typewriter => {
          typewriter.typeString(
            'Explore articles, tutorials and ideas shared by developers around the world.'
          ).start()
            .pauseFor(2000)
            .deleteAll().
            typeString('CodeCraft - a Place For Self Development')
            .start()
            .pauseFor(2000)
            .deleteAll()
        }} />

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