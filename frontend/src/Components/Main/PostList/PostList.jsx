import React, { useEffect, useState } from "react";
import BACKEND_URL from "../../../Utils";
import { Link } from "react-router-dom";
import "./PostList.css";

export default function PostList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const getPosts = async () => {
      try {
        const res = await fetch(
          `${BACKEND_URL}/blog/api/v1/post/`,
          {
            credentials: "include",
          }
        );

        if (!res.ok) {
          throw new Error("Failed to fetch posts");
        }

        const data = await res.json();

        console.log(data);

        if (Array.isArray(data)) {
          setPosts(data);
        } else if (Array.isArray(data.results)) {
          setPosts(data.results);
        } else {
          setPosts([]);
        }
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    getPosts();
  }, []);

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (error) {
    return <h2>{error}</h2>;
  }

  return (
    <div className="posts-container">
      <h2 className="posts-title">Latest Posts</h2>

      <div className="posts-grid">
        {posts.map((post) => (
          <div className="post-card" key={post.id}>
            <img
              className="post-image"
              src={post.image || "/images/default_image.PNG"}
              alt={post.title}
              onError={(e) => {
                e.target.src = "/images/default_image.PNG";
              }}
            />

            <h3>{post.title}</h3>

            <p>{post.snippet}</p>

            <p>{post.created_date}</p>

            <Link to={`/post/${post.id}`}>
              Detail
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}