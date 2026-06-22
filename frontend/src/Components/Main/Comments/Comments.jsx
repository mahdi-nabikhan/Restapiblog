import React, { useState, useContext } from "react";
import "./Comments.css";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AuthContext } from "../../../Context/AuthContex";
import BACKEND_URL from "../../../Utils";

export default function Comments({ id }) {
  const queryClient = useQueryClient();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComment, setSelectedComment] = useState(null);
  const [replyText, setReplyText] = useState("");
  const [content, setContent] = useState("");
  const [message, setMessage] = useState("");

  const { isLoggedIn } = useContext(AuthContext);

  // ======================
  // GET COMMENTS
  // ======================
  const getComments = async () => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/comments/${id}/`,
      {
        method: "GET",
        credentials: "include",
      }
    );

    if (!res.ok) throw new Error("Failed to fetch comments");

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
          body: JSON.stringify({ content }),
        }
      );

      if (!res.ok) throw new Error("Failed to add comment");

      return res.json();
    },
    onSuccess: () => {
      setContent("");
      setMessage("Comment added successfully ✅");
      queryClient.invalidateQueries(["comments", id]);
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
        `${BACKEND_URL}/blog/api/v1/comment/${selectedComment.id}/reply/`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: replyText }),
        }
      );

      if (!res.ok) throw new Error("Failed to send reply");

      return res.json();
    },
    onSuccess: () => {
      setReplyText("");
      setIsModalOpen(false);
      queryClient.invalidateQueries(["comments", id]);
    },
  });

  // ======================
  // UI HANDLERS
  // ======================
  const submitComment = () => {
    if (!content.trim()) return setMessage("Comment cannot be empty");
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
  if (error) return <h3>Error loading comments</h3>;

  return (
    <section className="comments-wrapper">

      {/* Add Comment */}
      {isLoggedIn ? (
        <div className="add-comment">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your comment..."
          />

          <button onClick={submitComment}>
            Submit Comment
          </button>

          {message && <p>{message}</p>}
        </div>
      ) : (
        <p>You must be logged in to write a comment.</p>
      )}

      {/* Comments */}
      <div className="comments">
        <h2>Comments ({comments.length})</h2>

        {comments.map((comment) => (
          <div key={comment.id}>
            <p>{comment.content}</p>
            <button onClick={() => openReplyModal(comment)}>
              Reply
            </button>
          </div>
        ))}
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">

            <textarea
              value={replyText}
              onChange={(e) => setReplyText(e.target.value)}
            />

            <button onClick={closeModal}>Close</button>
            <button onClick={sendReply}>Send Reply</button>

          </div>
        </div>
      )}
    </section>
  );
}