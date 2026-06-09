import React from 'react'
import { useParams } from "react-router-dom";
import PostDetail from '../../../Components/Main/PostDetail/PostDetail';

export default function PostDetailPages() {
    const {id}=useParams()
  return (
    <>
    <PostDetail id={id}/>
    </>
    
  )
}
