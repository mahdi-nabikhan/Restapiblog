import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./PostDetail.css";

const DEFAULT_IMAGE = "/images/default_image.PNG";

export default function PostDetail() {
  const { id } = useParams();

  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const getPostDetail = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/blog/api/v1/post/${id}/`,
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch post");
      }

      const data = await res.json();
      setPost(data);
    } catch (err) {
      setError("Failed to load post.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getPostDetail();
  }, [id]);

  if (loading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!post) return <div className="empty">Post not found</div>;

  return (
    <div className="post-container">
      <div className="post-card">
        <div className="post-layout">

          {/* Image */}
          <img
            className="post-image"
            src={post?.image || DEFAULT_IMAGE}
            alt={post?.title || "Post image"}
            onError={(e) => {
              e.target.src = DEFAULT_IMAGE;
            }}
          />

          {/* Content */}
          <div className="post-content">
            <h1 className="post-title">{post.title}</h1>

            <div className="post-meta">
              <span>
                Category: <b>{post.category?.name || "Uncategorized"}</b>
              </span>
              <span>
                Status: <b>{post.status ? "Published" : "Draft"}</b>
              </span>
            </div>

            <div className="post-dates">
              <span>
                Created:{" "}
                {new Date(post.created_date).toLocaleDateString()}
              </span>
              <span>
                Updated:{" "}
                {new Date(post.updated_date).toLocaleDateString()}
              </span>
            </div>

            <p className="post-text">{post.content}</p>
          </div>
        </div>
      </div>
    </div>
  );
}