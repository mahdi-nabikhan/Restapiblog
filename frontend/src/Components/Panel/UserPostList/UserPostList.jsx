import React from 'react'
import './UserPostList.css'
import { useQuery } from '@tanstack/react-query'
import BACKEND_URL from "../../../Utils";
export default function UserPostList() {
   const UserPosts= async function(){
      const res = await fetch (`${BACKEND_URL}//blog/api/v1/user/post/`,{
        credentials:'include'
      })
      const data = await res.json();
      console.log(data);
      return data;
   }


   const { data, isLoading, error } = useQuery({
    queryKey: ["posts"],
    queryFn: UserPosts,
  });


  
  if (isLoading) return <h2>Loading...</h2>;

if (error) return <h2>Error...</h2>;

return (
  <table className="posts-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Author</th>
        <th>Date</th>
        <th>Actions</th>
      </tr>
    </thead>

    <tbody>
      {data?.map((post) => (
        <tr key={post.id}>
          <td>{post.id}</td>
          <td>{post.title}</td>
          <td>{post.author}</td>
          <td>{post.created_date}</td>

          <td>
            <button>Edit</button>
            <button>Delete</button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
);
}
