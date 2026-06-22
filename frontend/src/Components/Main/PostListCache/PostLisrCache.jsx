import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import './PostListCache.css'
import { Link } from "react-router-dom";
import BACKEND_URL from "../../../Utils";
const fetchPosts = async () => {
  const res = await fetch(
    `${BACKEND_URL}/blog/api/v1/post/list/cache/`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch posts");
  }

  return res.json();
};

const PostListCache = () => {
  const { data: posts = [], isLoading, error } = useQuery({
    queryKey: ["cached-posts"],
    queryFn: fetchPosts,
    staleTime: 1000 * 60 * 5, 
  });

  if (isLoading) return <p>Loading posts...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  return (
      <div className="container">
        <h2 className="title">Other  Posts</h2>
    
        <div className="grid">
          {posts.map((post) => (
            <div key={post.id} className="card">
              <Link to= {`post/${post.id}`}>{post.title}</Link>
    
              <p className="cardText">
                {post.content?.slice(0, 120)}
                {post.content?.length > 120 && "..."}
              </p>
    
              <small className="date">
                {post.created_at &&
                  new Date(post.created_at).toLocaleDateString()}
              </small>
            </div>
          ))}
        </div>
      </div>

  );
};


export default PostListCache;