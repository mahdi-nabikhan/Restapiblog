import React, { useEffect, useState } from "react";
import "./Comments.css";
import CommentCard from "../CommentCard/CommentCard";

export default function Comments({ id }) {
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComment, setSelectedComment] = useState(null);

  const [replyText, setReplyText] = useState("");
  const [content, setContent] = useState("");
  const [message, setMessage] = useState("");

  const getComments = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/blog/api/v1/comments/${id}/`,
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch comments");
      }

      const data = await res.json();
      setComments(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const submitComment = async () => {
    if (!content.trim()) {
      setMessage("Comment cannot be empty");
      return;
    }

    try {
      setMessage("");

      const res = await fetch(
        `http://localhost:8000/blog/api/v1/comments/${id}/`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            content,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data?.message || "Failed to create comment"
        );
      }

      setMessage("Comment added successfully ✅");
      setContent("");

      getComments();
    } catch (error) {
      setMessage(error.message);
    }
  };

  useEffect(() => {
    if (id) {
      getComments();
    }
  }, [id]);

  const openReplyModal = (comment) => {
    setSelectedComment(comment);
    setReplyText("");
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setSelectedComment(null);
    setReplyText("");
    setIsModalOpen(false);
  };

  const sendReply = async () => {
    if (!replyText.trim()) return;

    try {
      const res = await fetch(
        `http://localhost:8000/blog/api/v1/comment/${selectedComment.id}/reply/`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            content: replyText,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Failed to send reply");
      }

      closeModal();
      getComments();
    } catch (error) {
      console.log(error);
    }
  };

  if (loading) {
    return <h3>Loading comments...</h3>;
  }

  return (
    <>
      <div className="add-comment">
        <h3>Leave a Comment</h3>

        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your comment..."
          className="add-comment__textarea"
        />

        <button
          className="add-comment__btn"
          onClick={submitComment}
        >
          Submit Comment
        </button>

        {message && (
          <p className="comment-message">
            {message}
          </p>
        )}
      </div>

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
              <h3>
                Reply to{" "}
                {selectedComment?.author ||
                  selectedComment?.name ||
                  "User"}
              </h3>

              <p className="parent-comment">
                {selectedComment?.content}
              </p>

              <textarea
                value={replyText}
                onChange={(e) =>
                  setReplyText(e.target.value)
                }
                placeholder="Write your reply..."
              />

              <div className="modal-actions">
                <button onClick={closeModal}>
                  Close
                </button>

                <button onClick={sendReply}>
                  Send Reply
                </button>
              </div>
            </div>
          </div>
        )}
      </section>
    </>
  );
}