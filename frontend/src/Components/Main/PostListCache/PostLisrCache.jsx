import { useEffect, useState } from "react";
import './PostListCache.css'
import { Link } from "react-router-dom";
const PostListCache = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPosts = async () => {
    try {
      setLoading(true);

      const res = await fetch("http://localhost:8000/blog/api/v1/post/list/cache/");

      if (!res.ok) {
        throw new Error("Failed to fetch posts");
      }

      const data = await res.json();

      setPosts(data);
      setError(null);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  if (loading) return <p>Loading posts...</p>;

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
      <div className="container">
        <h2 className="title">Other  Posts</h2>
    
        <div className="grid">
          {posts.map((post) => (
            <div key={post.id} className="card">
              <Link to= {`post/${post.id}`}>{post.title}</Link>
    
              <p className="cardText">
                {post.content?.slice(0, 120)}
                {post.content?.length > 120 && "..."}
              </p>
    
              <small className="date">
                {post.created_at &&
                  new Date(post.created_at).toLocaleDateString()}
              </small>
            </div>
          ))}
        </div>
      </div>

  );
};


export default PostListCache;