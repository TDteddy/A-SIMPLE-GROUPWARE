import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './PostForm.css'

function PostCreate() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    is_pinned: false,
    is_notice: false,
  })
  const [submitting, setSubmitting] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.title.trim()) {
      alert('제목을 입력해주세요.')
      return
    }

    if (!formData.content.trim()) {
      alert('내용을 입력해주세요.')
      return
    }

    setSubmitting(true)

    try {
      const response = await api.post('/posts/', formData)
      alert('게시글이 작성되었습니다.')
      navigate(`/posts/${response.data.id}`)
    } catch (error) {
      console.error('Failed to create post:', error)
      alert('게시글 작성에 실패했습니다.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="post-form-container">
      <h2>게시글 작성</h2>
      <form onSubmit={handleSubmit} className="post-form">
        <div className="form-group">
          <label htmlFor="title">제목</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="제목을 입력하세요"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="content">내용</label>
          <textarea
            id="content"
            name="content"
            value={formData.content}
            onChange={handleChange}
            placeholder="내용을 입력하세요"
            rows="15"
            required
          />
        </div>

        {user?.is_admin && (
          <div className="form-options">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="is_notice"
                checked={formData.is_notice}
                onChange={handleChange}
              />
              <span>공지사항</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="is_pinned"
                checked={formData.is_pinned}
                onChange={handleChange}
              />
              <span>상단 고정</span>
            </label>
          </div>
        )}

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate('/posts')}
            className="button button-secondary"
            disabled={submitting}
          >
            취소
          </button>
          <button
            type="submit"
            className="button button-primary"
            disabled={submitting}
          >
            {submitting ? '작성 중...' : '작성하기'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default PostCreate
