import React, { useState } from "react";
import "./AddPosts.css";

export default function AddPosts() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const submitHandler = async (e) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("content", content);

      if (image) {
        formData.append("image", image);
      }

      const res = await fetch(
        "http://localhost:8000/blog/api/v1/post/",
        {
          method: "POST",
          credentials: "include", 
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error("Failed to create post");
      }

      setTitle("");
      setContent("");
      setImage(null);

      setMessage("Post created successfully 🚀");
    } catch (err) {
      setMessage("Error creating post ❌");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-post-container">
      <form className="create-post-form" onSubmit={submitHandler}>
        <h2>Create New Post</h2>

        <input
          type="text"
          placeholder="Post title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          placeholder="Write your content..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <input
          type="file"
          onChange={(e) => setImage(e.target.files[0])}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Publishing..." : "Publish Post"}
        </button>

        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
}