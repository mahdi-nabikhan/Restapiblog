import React from 'react'
import { useParams } from "react-router-dom";
import PostDetail from '../../../Components/Main/PostDetail/PostDetail';
import Comments from '../../../Components/Main/Comments/Comments';

export default function PostDetailPages() {
    const {id}=useParams()
  return (
    <>
    <PostDetail id={id}/>
    <Comments/>
    </>
    
  )
}
