import { useEffect, useState } from "react";
import './PostListCache.css'
const PostListCache = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPosts = async () => {
    try {
      setLoading(true);

      const res = await fetch("http://localhost:8000/api/v1/post/list/");

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
    <div style={styles.container}>
      <h2>Random Posts (Cache)</h2>

      <div style={styles.grid}>
        {posts.map((post) => (
          <div key={post.id} style={styles.card}>
            <h3>{post.title}</h3>
            <p>
              {post.content?.slice(0, 120)}
              {post.content?.length > 120 && "..."}
            </p>

            <small>
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