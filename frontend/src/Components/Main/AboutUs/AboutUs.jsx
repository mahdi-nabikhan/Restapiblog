import "./AboutUs.css";

export default function AboutUs() {
  return (
    <section className="about">
      <div className="about__container">

        <div className="about__hero">
          <h1>About Our Blog</h1>

          <p>
            Welcome to MyBlog — a place where knowledge,
            technology, creativity, and personal experiences
            come together.
          </p>
        </div>

        <div className="about__content">

          <div className="about__card">
            <h2>Who We Are</h2>

            <p>
              We are passionate writers and developers who
              enjoy sharing useful content with people around
              the world. Our mission is to make learning
              easier and more accessible for everyone.
            </p>
          </div>

          <div className="about__card">
            <h2>Our Mission</h2>

            <p>
              Our goal is to publish high-quality articles,
              tutorials, guides, and insights that help
              readers improve their skills and stay updated
              with modern technologies and trends.
            </p>
          </div>

          <div className="about__card">
            <h2>What You'll Find Here</h2>

            <ul>
              <li>Technology Articles</li>
              <li>Programming Tutorials</li>
              <li>Development Tips</li>
              <li>Personal Experiences</li>
              <li>Latest Industry News</li>
            </ul>
          </div>

        </div>

        <div className="about__stats">

          <div className="stat">
            <h3>100+</h3>
            <p>Articles</p>
          </div>

          <div className="stat">
            <h3>50+</h3>
            <p>Authors</p>
          </div>

          <div className="stat">
            <h3>10K+</h3>
            <p>Readers</p>
          </div>

        </div>

      </div>
    </section>
  );
}