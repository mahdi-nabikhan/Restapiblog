import React, { useEffect, useState } from "react";
import BACKEND_URL from "../../../Utils";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import "./PostList.css";
import Pagination from "../../../Components/Pagination/Pagination";
export default function PostList() {

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 1;

  const getPosts = async (page) => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/post/?page=${page}&page_size=${pageSize}`,
      {
        credentials: "include",
      }
    );
  
    return res.json();
  };
  const { data, isLoading, error } = useQuery({
    queryKey: ["posts", page],
    queryFn: () => getPosts(page),
  });
  useEffect(() => {
    if (data?.count) {
      setTotalPages(Math.ceil(data.count / pageSize));
    }
  }, [data]);

  return (
    <div className="posts-container">
      <h2 className="posts-title">Latest Posts</h2>

      <div className="posts-grid">
        {data?.results?.map((post) => (
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
      <Pagination
        currentPage={page}
        totalPages={totalPages}
        onPageChange={setPage}
      />
    </div>
  );
}