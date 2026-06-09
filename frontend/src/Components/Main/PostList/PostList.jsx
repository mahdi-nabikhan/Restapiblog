import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./PostList.css";

export default function PostList() {
  const [posts,setPosts]=useState([])

  const fetchPosts = async () => {
    try {
      const res = await fetch(
        "http://localhost:8000/blog/api/v1/post/",
        {
          credentials:'include',
          method: "GET",
        }
      );

      const data = await res.json();
      setPosts(data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);


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

        <h3>Title : {post.title}</h3>

        <p>
          Description : {post.snippet}
        </p>
        <p>Published at : {post.created_date}</p>
        
        <Link to={`post/${post.id}`}>Detail</Link>
        
      </div>
    ))}
  </div>
</div>
  );
}