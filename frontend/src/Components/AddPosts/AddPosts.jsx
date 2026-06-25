import React, { useState } from "react";
import "./AddPosts.css";
import BACKEND_URL from "../../Utils";
import { useForm } from 'react-hook-form'
import { useMutation } from "@tanstack/react-query";

const createPost = async (data) => {
  const formData = new FormData();

  formData.append("title", data.title);
  formData.append("content", data.content);

  if (data.image?.[0]) {
    formData.append("image", data.image[0]);
  }

  const res = await fetch(
    `${BACKEND_URL}/blog/api/v1/post/`,
    {
      method: "POST",
      credentials: "include",
      body: formData,
    }
  );

  if (!res.ok) {
    throw new Error("Failed to create post");
  }

  return res.json();
};

export default function AddPosts() {


  const [message, setMessage] = useState("");
  const { register, handleSubmit, reset, formState: { errors } } = useForm()
  const mutation = useMutation({
    mutationFn: createPost,
    onSuccess: () => { reset(), setMessage('Post created successfully 🚀') },
    
    onError: () => { reset(), setMessage("Error creating post ❌") }
  })
  const submitHandler = (data) => {



    setMessage("");
    mutation.mutate(data)

  };

  return (
    <div className="create-post-container">
      <form className="create-post-form" onSubmit={handleSubmit(submitHandler)}>
        <h2>Create New Post</h2>

        <input
          type="text"
          placeholder="Post title"
          {...register("title", {
            required: "Title is required",
            minLength: {
              value: 3,
              message: "Title must be at least 3 characters",
            },
          })}
        />
        {errors.title && (
          <p className="error-message">
            {errors.title.message}
          </p>
        )}

        <textarea
          placeholder="Write your content..."
          {...register("content", {
            required: "Content is required",
            minLength: {
              value: 10,
              message: "Content must be at least 10 characters",
            },
          })}
        />
        {errors.content && (
          <p className="error-message">
            {errors.content.message}
          </p>
        )}
        <input
          type="file"
          accept="image/*"
          {...register("image")}
        />


        <button
          type="submit"
          disabled={mutation.isPending}
        >
          {mutation.isPending
            ? "Publishing..."
            : "Publish Post"}
        </button>

        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
}