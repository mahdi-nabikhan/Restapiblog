import React, { useEffect, useState, useContext } from "react";
import "./Comments.css";
import CommentCard from "../CommentCard/CommentCard";
import { AuthContext } from "../../../Context/AuthContex";


export default function Comments({ id }) {
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComment, setSelectedComment] = useState(null);

  const [replyText, setReplyText] = useState("");
  const [content, setContent] = useState("");
  const [message, setMessage] = useState("");
  const { user, isLoggedIn, loading: authLoading } =
    useContext(AuthContext);

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
      <section className="comments-wrapper">
        {/* Add Comment Section */}
        {isLoggedIn ? (
          <div className="add-comment">
            <h3 className="add-comment__title">Leave a Comment</h3>

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
              <p className="add-comment__message">
                {message}
              </p>
            )}
          </div>
        ) : (
          <div className="comment-login-box">
            <p>You must be logged in to write a comment.</p>
          </div>
        )}

        {/* Comments List */}
        <div className="comments">
          <h2 className="comments__title">
            Comments ({comments.length})
          </h2>

          <div className="comments__list">
            {comments.map((comment) => (
              <div key={comment.id} className="comment-card">
                <div className="comment-card__header">
                  <span className="comment-card__author">
                    {comment.author || "User"}
                  </span>

                  <span className="comment-card__date">
                    {comment.created_at}
                  </span>
                </div>

                <p className="comment-card__content">
                  {comment.content}
                </p>

                <button
                  className="comment-card__reply"
                  onClick={() => openReplyModal(comment)}
                >
                  Reply
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Reply Modal */}
        {isModalOpen && (
          <div className="modal-overlay">
            <div className="modal">
              <h3>Reply to Comment</h3>

              <p className="modal__parent">
                {selectedComment?.content}
              </p>

              <textarea
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder="Write your reply..."
                className="modal__textarea"
              />

              <div className="modal__actions">
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