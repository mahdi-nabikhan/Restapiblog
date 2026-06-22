import React, { useEffect, useState } from "react";
import "./PostDetail.css";
import BACKEND_URL from "../../../Utils";
import { useQuery } from "@tanstack/react-query";
const DEFAULT_IMAGE = "/images/default_image.PNG";

export default function PostDetail({ id }) {

  const getPostDetail = async () => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/post/${id}/`,
      {
        method: "GET",
        credentials: "include",
      }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch post");
    }

    return res.json();
  };


  const { data, isLoading, error } = useQuery({
    queryKey: ['post', id],
    queryFn: getPostDetail,
    enabled: !!id
  })
  const imageUrl =
    data?.image
      ? data.image.startsWith("http")
        ? data.image
        : `http://${BACKEND_URL}${data?.image}`
      : DEFAULT_IMAGE;

  if (isLoading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!data) return <div className="empty">Post not found</div>;



  return (
    <div className="post-container">
      <div className="post-card">
        <div className="post-layout">

          {/* Image */}
          <img
            className="post-image"
            src={imageUrl}
            alt={data?.title || "Post image"}
            onError={(e) => {
              e.target.onerror = null; // جلوگیری از loop
              e.target.src = DEFAULT_IMAGE;
            }}
          />

          {/* Content */}
          <div className="post-content">
            <h1 className="post-title">{data.title}</h1>

            <div className="post-meta">
              <span>
                Category: <b>{data?.category?.name || "Uncategorized"}</b>
              </span>
              <span>
                Status: <b>{data?.status ? "Published" : "Draft"}</b>
              </span>
            </div>

            <div className="post-dates">
              <span>
                Created:{" "}
                {new Date(data?.created_date).toLocaleDateString()}
              </span>
              <span>
                Updated:{" "}
                {new Date(data?.updated_date).toLocaleDateString()}
              </span>
            </div>

            <p className="post-text">{data?.content}</p>
          </div>
        </div>
      </div>
    </div>
  );
}