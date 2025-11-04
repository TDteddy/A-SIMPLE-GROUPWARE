import { useState, useEffect } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './AdminDashboard.css'

function AdminDashboard() {
  const location = useLocation()
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 대시보드 메인 페이지일 때만 통계 로드
    if (location.pathname === '/admin') {
      fetchStats()
    }
  }, [location.pathname])

  const fetchStats = async () => {
    try {
      const response = await api.get('/admin/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  // 관리자가 아닌 경우
  if (!user?.is_admin) {
    return (
      <div className="admin-error">
        <h2>접근 권한이 없습니다</h2>
        <p>관리자만 접근할 수 있는 페이지입니다.</p>
        <Link to="/">홈으로 돌아가기</Link>
      </div>
    )
  }

  return (
    <div className="admin-container">
      <div className="admin-sidebar">
        <h2>관리자 페이지</h2>
        <nav className="admin-nav">
          <Link
            to="/admin"
            className={location.pathname === '/admin' ? 'active' : ''}
          >
            📊 대시보드
          </Link>
          <Link
            to="/admin/users"
            className={location.pathname === '/admin/users' ? 'active' : ''}
          >
            👥 사용자 관리
          </Link>
          <Link
            to="/admin/posts"
            className={location.pathname === '/admin/posts' ? 'active' : ''}
          >
            📝 게시글 관리
          </Link>
          <Link to="/" className="back-link">
            ← 메인으로
          </Link>
        </nav>
      </div>

      <div className="admin-content">
        {location.pathname === '/admin' ? (
          <div className="admin-dashboard">
            <h1>대시보드</h1>
            {loading ? (
              <div className="loading">로딩 중...</div>
            ) : stats ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">👥</div>
                  <div className="stat-info">
                    <h3>전체 사용자</h3>
                    <p className="stat-number">{stats.total_users}</p>
                    <p className="stat-detail">
                      활성: {stats.active_users}
                    </p>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon">📝</div>
                  <div className="stat-info">
                    <h3>전체 게시글</h3>
                    <p className="stat-number">{stats.total_posts}</p>
                    <p className="stat-detail">
                      최근 7일: {stats.recent_posts_count}
                    </p>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon">👁️</div>
                  <div className="stat-info">
                    <h3>총 조회수</h3>
                    <p className="stat-number">
                      {stats.total_views.toLocaleString()}
                    </p>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon">✨</div>
                  <div className="stat-info">
                    <h3>신규 사용자</h3>
                    <p className="stat-number">{stats.recent_users_count}</p>
                    <p className="stat-detail">최근 7일</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="error">통계 데이터를 불러올 수 없습니다.</div>
            )}
          </div>
        ) : (
          <Outlet />
        )}
      </div>
    </div>
  )
}

export default AdminDashboard
