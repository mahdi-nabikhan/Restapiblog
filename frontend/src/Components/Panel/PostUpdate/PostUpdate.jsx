import React from 'react'
import './PostUpdate.css'
export default function PostUpdate() {
  return (
    <div class="update-post">
  <h2 class="update-post__title">Update Post</h2>

  <form class="update-post__form">

    <label>Title</label>
    <input type="text" placeholder="Enter post title" />

    <label>Content</label>
    <textarea placeholder="Write your content..."></textarea>

    <label>Image Preview</label>
    <div class="update-post__image-box">
      <img src="/images/default_image.PNG" alt="preview" />
    </div>

    <label>Change Image</label>
    <input type="file" />

    <button type="submit">Update Post</button>

  </form>
</div>
  )
}
