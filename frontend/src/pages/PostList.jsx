import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'
import api from '../services/api'
import './PostList.css'

function PostList() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    try {
      const response = await api.get('/posts/')
      setPosts(response.data)
    } catch (error) {
      console.error('Failed to fetch posts:', error)
      alert('게시글을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'yyyy.MM.dd HH:mm', { locale: ko })
    } catch {
      return dateString
    }
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  return (
    <div className="post-list-container">
      <div className="post-list-header">
        <h2>게시판</h2>
        <Link to="/posts/new" className="create-button">
          글쓰기
        </Link>
      </div>

      <div className="post-list">
        {posts.length === 0 ? (
          <div className="empty-state">
            <p>게시글이 없습니다.</p>
            <Link to="/posts/new" className="create-button">
              첫 게시글 작성하기
            </Link>
          </div>
        ) : (
          <div className="post-table">
            <div className="post-table-header">
              <div className="post-col-title">제목</div>
              <div className="post-col-author">작성자</div>
              <div className="post-col-date">작성일</div>
              <div className="post-col-views">조회수</div>
            </div>
            {posts.map((post) => (
              <Link
                key={post.id}
                to={`/posts/${post.id}`}
                className="post-row"
              >
                <div className="post-col-title">
                  {post.is_notice && (
                    <span className="badge badge-notice">공지</span>
                  )}
                  {post.is_pinned && (
                    <span className="badge badge-pinned">📌</span>
                  )}
                  {post.title}
                </div>
                <div className="post-col-author">
                  {post.author_picture && (
                    <img
                      src={post.author_picture}
                      alt={post.author_name}
                      className="author-avatar"
                    />
                  )}
                  <span>{post.author_name}</span>
                </div>
                <div className="post-col-date">
                  {formatDate(post.created_at)}
                </div>
                <div className="post-col-views">{post.view_count}</div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default PostList
