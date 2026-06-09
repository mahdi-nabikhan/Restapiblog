import React from "react";
import "./Comments.css";

export default function Comments() {
  const comments = [
    {
      id: 1,
      username: "John Doe",
      date: "Aug 15, 2026",
      content:
        "This article was really helpful. I learned several new things about React.",
    },
    {
      id: 2,
      username: "Sarah Smith",
      date: "Aug 16, 2026",
      content:
        "Great explanation. Looking forward to more posts like this!",
    },
    {
      id: 3,
      username: "Michael Brown",
      date: "Aug 17, 2026",
      content:
        "The examples were simple and easy to understand. Thanks for sharing.",
    },
  ];

  return (
    <section className="comments">
      <h2 className="comments__title">
        Comments ({comments.length})
      </h2>

      <div className="comments__list">
        {comments.map((comment) => (
          <div className="comment-card" key={comment.id}>
            <div className="comment-card__header">
              <div className="comment-card__avatar">
                {comment.username.charAt(0)}
              </div>

              <div>
                <h4>{comment.username}</h4>
                <span>{comment.date}</span>
              </div>
            </div>

            <p className="comment-card__content">
              {comment.content}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}