import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'
import api from '../services/api'
import './AdminPosts.css'

function AdminPosts() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    try {
      const response = await api.get('/admin/posts')
      setPosts(response.data)
    } catch (error) {
      console.error('Failed to fetch posts:', error)
      alert('게시글 목록을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (postId, postTitle) => {
    if (!window.confirm(`"${postTitle}" 게시글을 삭제하시겠습니까?`)) {
      return
    }

    try {
      await api.delete(`/admin/posts/${postId}`)
      alert('게시글이 삭제되었습니다.')
      fetchPosts()
    } catch (error) {
      console.error('Failed to delete post:', error)
      alert('게시글 삭제에 실패했습니다.')
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
    <div className="admin-posts">
      <div className="admin-posts-header">
        <h1>게시글 관리</h1>
        <p className="post-count">총 {posts.length}개</p>
      </div>

      <div className="posts-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>제목</th>
              <th>작성자</th>
              <th>작성일</th>
              <th>조회수</th>
              <th>상태</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            {posts.map((post) => (
              <tr key={post.id}>
                <td>{post.id}</td>
                <td className="title-cell">
                  <div className="title-badges">
                    {post.is_notice && (
                      <span className="badge badge-notice">공지</span>
                    )}
                    {post.is_pinned && (
                      <span className="badge badge-pinned">고정</span>
                    )}
                  </div>
                  <Link to={`/posts/${post.id}`} className="post-title">
                    {post.title}
                  </Link>
                </td>
                <td>
                  <div className="author-info">
                    <span className="author-name">{post.author_name}</span>
                    <span className="author-email">{post.author_email}</span>
                  </div>
                </td>
                <td className="date-cell">{formatDate(post.created_at)}</td>
                <td className="views-cell">{post.view_count}</td>
                <td>
                  {post.is_notice ? (
                    <span className="status-badge notice">공지사항</span>
                  ) : post.is_pinned ? (
                    <span className="status-badge pinned">고정</span>
                  ) : (
                    <span className="status-badge normal">일반</span>
                  )}
                </td>
                <td>
                  <div className="action-buttons">
                    <Link
                      to={`/posts/${post.id}`}
                      className="btn-sm btn-view"
                    >
                      보기
                    </Link>
                    <Link
                      to={`/posts/${post.id}/edit`}
                      className="btn-sm btn-edit"
                    >
                      수정
                    </Link>
                    <button
                      onClick={() => handleDelete(post.id, post.title)}
                      className="btn-sm btn-delete"
                    >
                      삭제
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {posts.length === 0 && (
          <div className="empty-state">
            <p>게시글이 없습니다.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminPosts
