import React, { useState, useContext } from "react";
import "./Comments.css";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AuthContext } from "../../../Context/AuthContex";
import BACKEND_URL from "../../../Utils";

export default function Comments({ id }) {
  const queryClient = useQueryClient();

  const [content, setContent] = useState("");
  const [replyText, setReplyText] = useState("");
  const [selectedComment, setSelectedComment] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [message, setMessage] = useState("");

  const { isLoggedIn } = useContext(AuthContext);

  // ======================
  // GET COMMENTS
  // ======================

  const getComments = async () => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/comments/${id}/`,
      {
        credentials: "include",
      }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch comments");
    }

    return res.json();
  };

  const {
    data: comments = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["comments", id],
    queryFn: getComments,
    enabled: !!id,
  });

  // ======================
  // ADD COMMENT
  // ======================

  const addCommentMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(
        `${BACKEND_URL}/blog/api/v1/comments/${id}/`,
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

      if (!res.ok) {
        throw new Error("Failed to add comment");
      }

      return res.json();
    },

    onSuccess: () => {
      setContent("");
      setMessage("Comment added successfully ✅");

      queryClient.invalidateQueries({
        queryKey: ["comments", id],
      });
    },

    onError: (err) => {
      setMessage(err.message);
    },
  });

  // ======================
  // ADD REPLY
  // ======================

  const replyMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(
        `${BACKEND_URL}/blog/api/v1/comments/${id}/`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            content: replyText,
            parent: selectedComment.pk,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Failed to send reply");
      }

      return res.json();
    },

    onSuccess: () => {
      setReplyText("");
      setSelectedComment(null);
      setIsModalOpen(false);

      queryClient.invalidateQueries({
        queryKey: ["comments", id],
      });
    },
  });

  // ======================
  // HANDLERS
  // ======================

  const submitComment = () => {
    if (!content.trim()) {
      setMessage("Comment cannot be empty");
      return;
    }

    addCommentMutation.mutate();
  };

  const sendReply = () => {
    if (!replyText.trim()) return;

    replyMutation.mutate();
  };

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

  // ======================
  // LOADING
  // ======================

  if (isLoading) return <h3>Loading comments...</h3>;

  if (error) return <h3>{error.message}</h3>;

  // ======================
  // RENDER
  // ======================

  return (
    <section className="comments-wrapper">

      {isLoggedIn ? (
        <div className="add-comment">

          <textarea
            placeholder="Write your comment..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />

          <button
            disabled={addCommentMutation.isPending}
            onClick={submitComment}
          >
            {addCommentMutation.isPending
              ? "Submitting..."
              : "Submit Comment"}
          </button>

          {message && <p>{message}</p>}

        </div>
      ) : (
        <p>You must be logged in to write a comment.</p>
      )}

      <div className="comments">

        <h2>Comments ({comments.length})</h2>

        {comments.length === 0 && <p>No comments yet.</p>}

        {comments.map((comment) => (
          <div
            key={comment.pk}
            className="comment-card"
          >
            <p>{comment.content}</p>

            <button
              onClick={() => openReplyModal(comment)}
            >
              Reply
            </button>

            {/* اگر این کامنت Reply باشد */}
            {comment.parent && (
              <div
                style={{
                  marginTop: "10px",
                  marginLeft: "20px",
                  paddingLeft: "10px",
                  borderLeft: "2px solid #ddd",
                }}
              >
                <small>Reply to:</small>
                <p>{comment.parent.content}</p>
              </div>
            )}
          </div>
        ))}

      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">

            <h3>Reply</h3>

            <p>
              Replying to:
              <br />
              <strong>{selectedComment?.content}</strong>
            </p>

            <textarea
              value={replyText}
              onChange={(e) => setReplyText(e.target.value)}
              placeholder="Write your reply..."
            />

            <button onClick={closeModal}>
              Cancel
            </button>

            <button
              disabled={replyMutation.isPending}
              onClick={sendReply}
            >
              {replyMutation.isPending
                ? "Sending..."
                : "Send Reply"}
            </button>

          </div>
        </div>
      )}

    </section>
  );
}