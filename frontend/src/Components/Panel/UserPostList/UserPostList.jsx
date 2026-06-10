import React from 'react'
import './UserPostList.css'
export default function UserPostList() {
  return (
    <>
        <div class="user-posts-wrapper">

<div class="user-posts">

  <h2 class="user-posts__title">My Posts</h2>

  <div class="user-posts__list">

    <div class="post-item">
      <img src="/images/default_image.PNG" />

      <div class="post-info">
        <h3>Post Title</h3>
        <p>Short snippet of post content...</p>

        <div class="post-meta">
          <span>Tech</span>
          <span>Published</span>
        </div>
      </div>

      <div class="post-actions">
        <button>Edit</button>
        <button>Delete</button>
      </div>
    </div>

  </div>

</div>

</div>
    
    </>
  )
}
