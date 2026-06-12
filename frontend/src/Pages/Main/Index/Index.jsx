import React from 'react'
import PostList from '../../../Components/Main/PostList/PostList'
import MainBar from '../../../Components/Main/Mainbar/Mainbar'
import PostListCache from '../../../Components/Main/PostListCache/PostLisrCache'
export default function Index() {
  return (
    <>
    <MainBar/>
    <PostList/>
    <PostListCache/>
    </>
  )
}
