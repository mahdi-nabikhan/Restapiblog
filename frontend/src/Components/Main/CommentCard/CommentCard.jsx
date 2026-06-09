import './CommentCard.css'

export default function CommentCard({ comment, onReply }) {
    return (
      <div className="comment-card">
        <h4>{comment.username}</h4>
  
        <p>{comment.content}</p>
  
        <button
          className="reply-btn"
          onClick={onReply}
        >
          Reply
        </button>
      </div>
    );
  }