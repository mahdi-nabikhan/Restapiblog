import React, { useState } from "react";
import "./Comments.css";
import CommentCard from "../CommentCard/CommentCard";

export default function Comments() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComment, setSelectedComment] = useState(null);

  const openReplyModal = (comment) => {
    setSelectedComment(comment);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setSelectedComment(null);
    setIsModalOpen(false);
  };

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
      content: "Great explanation. Looking forward to more posts like this!",
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
          <CommentCard
            key={comment.id}
            comment={comment}
            onReply={() => openReplyModal(comment)}
          />
        ))}
      </div>

      
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Reply to {selectedComment?.username}</h3>

            <p style={{ marginBottom: "10px" }}>
              {selectedComment?.content}
            </p>

            <textarea placeholder="Write your reply..." />

            <div className="modal-actions">
              <button onClick={closeModal}>Close</button>
              <button>Send</button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}