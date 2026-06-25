import React from 'react'
import './UserPostList.css'
import { useQuery } from '@tanstack/react-query'
import BACKEND_URL from "../../../Utils";
import { Link } from 'react-router-dom';
export default function UserPostList() {
   const UserPosts= async function(){
      const res = await fetch (`${BACKEND_URL}/blog/api/v1/user/post/`,{
        credentials:'include'
      })
      const data = await res.json();
      console.log(data);
      return data;
   }


   const { data, isLoading, error } = useQuery({
    queryKey: ["posts"],
    queryFn: UserPosts,
  });


  
  if (isLoading) return <h2>Loading...</h2>;

if (error) return <h2>Error...</h2>;

return (
  <div className="user-posts-container">
  <div className="user-posts-header">
    <h1>My Posts</h1>
    <Link className="add-post-btn" to="/add/post">
      + New Post
    </Link>
  </div>

  <div className="posts-grid">
    {data?.map((post) => (
      <div className="post-card" key={post.id}>
        <div className="post-card-header">
          <h3>{post.title}</h3>
          <span className="post-id">#{post.id}</span>
        </div>

        <p className="post-description">
          {post.snippet || "No description available"}
        </p>

        <div className="post-meta">
          <span>👤 {post.author}</span>
          <span>📅 {post.created_date}</span>
        </div>

        <div className="post-actions">
          <Link
            className="edit-btn"
            to={`/panel/post/${post.id}`}
          >
            Edit
          </Link>

          <button className="delete-btn">
            Delete
          </button>
        </div>
      </div>
    ))}
  </div>
</div>
);
}
