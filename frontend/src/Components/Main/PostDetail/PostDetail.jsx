import React from "react";
import "./PostDetail.css";
import BACKEND_URL from "../../../Utils";
import { useQuery } from "@tanstack/react-query";

import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";

import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

const DEFAULT_IMAGE = "/images/default_image.PNG";

export default function PostDetail({ id }) {

  const getPostDetail = async () => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/post/${id}/`,
      {
        credentials: "include",
      }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch post");
    }

    return res.json();
  };

  const getPostImages = async () => {
    const res = await fetch(
      `${BACKEND_URL}/blog/api/v1/img/post/${id}/`,
      {
        credentials: "include",
      }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch images");
    }

    return res.json();
  };

  const {
    data,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["post", id],
    queryFn: getPostDetail,
    enabled: !!id,
  });

  const {
    data: images = [],
    isLoading: imagesLoading,
    error: imagesError,
  } = useQuery({
    queryKey: ["post-images", id],
    queryFn: getPostImages,
    enabled: !!id,
  });

  if (isLoading || imagesLoading) {
    return <div className="loader">Loading...</div>;
  }

  if (error) {
    return <div className="error">{error.message}</div>;
  }

  if (imagesError) {
    return <div className="error">{imagesError.message}</div>;
  }

  if (!data) {
    return <div className="empty">Post not found</div>;
  }

  const allImages = [
    data?.image,
    ...images.map((img) => img.image),
  ].filter(Boolean);

  return (
    <div className="post-container">
      <div className="post-card">
        <div className="post-layout">

          {/* Swiper Slider */}
          <div className="post-slider">

            {allImages.length > 0 ? (
              <Swiper
                modules={[Navigation, Pagination]}
                navigation
                pagination={{ clickable: true }}
                spaceBetween={20}
                slidesPerView={1}
              >
                {allImages.map((image, index) => (
                  <SwiperSlide key={index}>
                    <img
                      className="post-image"
                      src={`http://localhost:8000${image}`}
                      alt={`post-${index}`}
                      onError={(e) => {
                        e.target.src = DEFAULT_IMAGE;
                      }}
                    />
                  </SwiperSlide>
                ))}
              </Swiper>
            ) : (
              <img
                className="post-image"
                src={DEFAULT_IMAGE}
                alt="default"
              />
            )}

          </div>

          {/* Content */}
          <div className="post-content">

            <h1 className="post-title">
              {data.title}
            </h1>

            <div className="post-meta">
              <span>
                Category:
                <b>
                  {" "}
                  {data?.category?.name || "Uncategorized"}
                </b>
              </span>

              <span>
                Status:
                <b>
                  {" "}
                  {data?.status ? "Published" : "Draft"}
                </b>
              </span>
            </div>

            <div className="post-dates">
              <span>
                Created:
                {" "}
                {new Date(
                  data.created_date
                ).toLocaleDateString()}
              </span>

              <span>
                Updated:
                {" "}
                {new Date(
                  data.updated_date
                ).toLocaleDateString()}
              </span>
            </div>

            <p className="post-text">
              {data.content}
            </p>

          </div>

        </div>
      </div>
    </div>
  );
}