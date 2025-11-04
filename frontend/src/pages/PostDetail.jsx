import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './PostDetail.css'

function PostDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPost()
  }, [id])

  const fetchPost = async () => {
    try {
      const response = await api.get(`/posts/${id}`)
      setPost(response.data)
    } catch (error) {
      console.error('Failed to fetch post:', error)
      alert('게시글을 불러오는데 실패했습니다.')
      navigate('/posts')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('정말 삭제하시겠습니까?')) {
      return
    }

    try {
      await api.delete(`/posts/${id}`)
      alert('게시글이 삭제되었습니다.')
      navigate('/posts')
    } catch (error) {
      console.error('Failed to delete post:', error)
      alert('게시글 삭제에 실패했습니다.')
    }
  }

  const formatDate = (dateString) => {
    try {
      return format(new Date(dateString), 'yyyy년 MM월 dd일 HH:mm', {
        locale: ko,
      })
    } catch {
      return dateString
    }
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  if (!post) {
    return <div className="error">게시글을 찾을 수 없습니다.</div>
  }

  const canEdit = user && (user.id === post.author_id || user.is_admin)

  return (
    <div className="post-detail-container">
      <div className="post-detail-header">
        <div className="post-badges">
          {post.is_notice && (
            <span className="badge badge-notice">공지</span>
          )}
          {post.is_pinned && (
            <span className="badge badge-pinned">고정</span>
          )}
        </div>
        <h1 className="post-title">{post.title}</h1>
        <div className="post-meta">
          <div className="post-author">
            {post.author_picture && (
              <img
                src={post.author_picture}
                alt={post.author_name}
                className="author-avatar"
              />
            )}
            <span>{post.author_name}</span>
          </div>
          <div className="post-info">
            <span>{formatDate(post.created_at)}</span>
            <span>조회 {post.view_count}</span>
          </div>
        </div>
      </div>

      <div className="post-content">
        <div
          className="post-body"
          dangerouslySetInnerHTML={{ __html: post.content.replace(/\n/g, '<br>') }}
        />
      </div>

      <div className="post-actions">
        <Link to="/posts" className="button button-secondary">
          목록으로
        </Link>
        {canEdit && (
          <div className="post-actions-right">
            <Link
              to={`/posts/${id}/edit`}
              className="button button-primary"
            >
              수정
            </Link>
            <button
              onClick={handleDelete}
              className="button button-danger"
            >
              삭제
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default PostDetail
