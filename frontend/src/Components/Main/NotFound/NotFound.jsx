import { Link } from "react-router-dom";


export default function NotFound() {
  return (
    <div className="not-found">
      <h1>404 🚧</h1>

      <h2>Hey! What are you looking for here?</h2>

      <p>
        This page doesn't exist... or maybe it never did.
      </p>

      <Link to="/">
        Take me home
      </Link>
    </div>
  );
}