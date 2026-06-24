import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import "./PostListCache.css";
import BACKEND_URL from "../../../Utils";

const fetchPosts = async () => {
  const res = await fetch(
    `${BACKEND_URL}/blog/api/v1/post/list/cache/`,
    {
      credentials: "include",
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch posts");
  }

  return await res.json();
};

const PostListCache = () => {
  const {
    data: posts = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["cached-posts"],
    queryFn: fetchPosts,
    staleTime: 1000 * 60 * 5,
    retry: false,
  });

  if (isLoading) {
    return <p>Loading posts...</p>;
  }

  if (error) {
    console.error(error);

    return (
      <p style={{ color: "red" }}>
        {error.message}
      </p>
    );
  }

  return (
    <div className="container">
      <h2 className="title">Other Posts</h2>

      <div className="grid">
        {posts.length === 0 ? (
          <p>No posts found.</p>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="card">
              <Link to={`/post/${post.id}`}>
                {post.title}
              </Link>

              <p className="cardText">
                {post.content?.slice(0, 120)}
                {post.content?.length > 120 && "..."}
              </p>

              <small className="date">
                {post.created_at
                  ? new Date(
                      post.created_at
                    ).toLocaleDateString()
                  : ""}
              </small>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default PostListCache;