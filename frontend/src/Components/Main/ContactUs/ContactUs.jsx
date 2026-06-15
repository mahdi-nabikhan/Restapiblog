import "./ContactUs.css";

export default function ContactUs() {
  return (
    <section className="contact">
      <div className="contact__container">

        <div className="contact__header">
          <h1>Contact Us</h1>
          <p>
            Have a question, suggestion, or feedback?
            We'd love to hear from you.
          </p>
        </div>

        <div className="contact__content">

          <div className="contact__info">
            <h2>Get In Touch</h2>

            <div className="contact__item">
              <span>📧</span>
              <p>support@myblog.com</p>
            </div>

            <div className="contact__item">
              <span>📞</span>
              <p>+1 234 567 890</p>
            </div>

            <div className="contact__item">
              <span>📍</span>
              <p>Baku, Azerbaijan</p>
            </div>
          </div>

          <form className="contact__form">
            <input
              type="text"
              placeholder="Your Name"
            />

            <input
              type="email"
              placeholder="Your Email"
            />

            <input
              type="text"
              placeholder="Subject"
            />

            <textarea
              rows="6"
              placeholder="Your Message"
            ></textarea>

            <button type="submit">
              Send Message
            </button>
          </form>

        </div>
      </div>
    </section>
  );
}