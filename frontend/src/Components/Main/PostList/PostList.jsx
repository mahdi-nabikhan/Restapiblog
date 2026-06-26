import React, { useEffect, useState } from "react";
import BACKEND_URL from "../../../Utils";
import { Link } from "react-router-dom";
import "./PostList.css";
import { useQuery } from "@tanstack/react-query";
export default function PostList() {
  async function  getPosts(){
    const res =await fetch(`${BACKEND_URL}/blog/api/v1/post` ,{
      credentials :'include'
    })
    data=await res.json()
    console.log(data)
    return data
    
  }
  const {data,isLoading,error} = useQuery({
    queryKey:['posts'],
    queryFn:getPosts
  })
  if (isLoading) {
    return <h2>Loading...</h2>;
  }

  if (error) {
    return <h2>{error.message}</h2>;
  }

  return (
    <div className="posts-container">
      <h2 className="posts-title">Latest Posts</h2>

      <div className="posts-grid">
        {data?.map((post) => (
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