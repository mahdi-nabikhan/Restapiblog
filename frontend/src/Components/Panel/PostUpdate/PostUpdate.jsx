import React, { useState } from 'react'
import './PostUpdate.css'
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import BACKEND_URL from '../../../Utils';
import { useParams } from 'react-router-dom';

const updatePost = async (data) => {
  const formData = new FormData();

  formData.append("title", data.title);
  formData.append("content", data.content);

  if (data.image?.[0]) {
    formData.append("image", data.image[0]);
  }
  const res = await fetch(`${BACKEND_URL}/blog/api/v1/post/detail/${data.id}`, {
    method: 'PUT',
    credentials: 'include',
    body: formData
  })
  const responseData = await res.json();
  if (!res.ok) {
    throw new Error(responseData?.detail ||"updateing a post is ")
  }
  return await res.json()
}

export default function PostUpdate() {
  const { id } = useParams();
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const { register, handleSubmit, formState: { errors }, } = useForm();
  const mutations = useMutation(
    {
      mutationFn: updatePost,
      onError: (error) => {
        setError(error.message)
      },
      onSuccess: () => { setSuccess('post successfully updated') }
    }
  )
  const submithandelr = (data) => {
    setError('')
    setSuccess('')
    mutations.mutate({
      title: data.title,
      content: data.content,
      image: data.image,
      id: id

    })
  }
  return (

    <div className="update-post">
      <h2 className="update-post__title">Update Post</h2>
      {error && <p className="error">{error}</p>}
{success && <p className="success">{success}</p>}
      <form className="update-post__form" onSubmit={handleSubmit(submithandelr)}>

        <label>Title</label>
        <input
          type="text"
          placeholder="Enter your title"
          {...register("title", {
            required: "title is required",
          })}
        />
        {errors.title && (
          <p>{errors.title.message}</p>
        )}

        <label>Content</label>
        <textarea
          type="text"
          placeholder="Enter your content"
          {...register("content", {
            required: "content is required",
          })}
        />
        {errors.content && (
          <p>{errors.content.message}</p>
        )}

        <label>Image Preview</label>
        <div className="update-post__image-box">
          <img src="/images/default_image.PNG" alt="preview" />
        </div>

        <label>Change Image</label>
        <input
          type="file"
          accept="image/*"
          {...register("image")}
        />

        <button
          type="submit"
          disabled={mutations.isPending}
        >
          {mutations.isPending
            ? "Updating..."
            : "Update Post"}
        </button>

      </form>
    </div>
  )
}
