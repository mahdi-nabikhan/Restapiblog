import React from "react";
import BACKEND_URL from "../../../Utils";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import "./PostList.css";

export default function PostList() {
  const getPosts = async () => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/post/`,
      {
        credentials: "include",
      }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch posts");
    }
    console.log(res.json())
    return res.json();

  };

  const { data, isLoading, error } = useQuery({
    queryKey: ["posts"],
    queryFn: getPosts,
  });

  if (isLoading) {
    return <h2>Loading...</h2>;
  }

  if (error) {
    return <h2>Error loading posts</h2>;
  }

  return (
    <div className="posts-container">
      <h2 className="posts-title">Latest Posts</h2>

      <div className="posts-grid">
        {(data?.results || data || []).map((post) => (
          <div className="post-card" key={post.id}>
            <img
              className="post-image"
              src={post.image || "/images/default_image.PNG"}
              alt={post.title}
              onError={(e) => {
                e.target.src = "/images/default_image.PNG";
              }}
            />

            <h3>Title: {post.title}</h3>

            <p>Description: {post.snippet}</p>

            <p>Published at: {post.created_date}</p>

            <Link to={`/post/${post.id}`}>
              Detail
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}