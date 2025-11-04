import { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'
import api from '../services/api'
import './AdminUsers.css'

function AdminUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await api.get('/admin/users')
      setUsers(response.data)
    } catch (error) {
      console.error('Failed to fetch users:', error)
      alert('사용자 목록을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleToggleAdmin = async (userId, currentStatus) => {
    const action = currentStatus ? '해제' : '부여'
    if (!window.confirm(`관리자 권한을 ${action}하시겠습니까?`)) {
      return
    }

    try {
      await api.patch(`/admin/users/${userId}`, {
        is_admin: !currentStatus,
      })
      alert('권한이 변경되었습니다.')
      fetchUsers()
    } catch (error) {
      console.error('Failed to update user:', error)
      alert('권한 변경에 실패했습니다.')
    }
  }

  const handleToggleActive = async (userId, currentStatus) => {
    const action = currentStatus ? '비활성화' : '활성화'
    if (!window.confirm(`계정을 ${action}하시겠습니까?`)) {
      return
    }

    try {
      await api.patch(`/admin/users/${userId}`, {
        is_active: !currentStatus,
      })
      alert('계정 상태가 변경되었습니다.')
      fetchUsers()
    } catch (error) {
      console.error('Failed to update user:', error)
      alert('계정 상태 변경에 실패했습니다.')
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
    <div className="admin-users">
      <div className="admin-users-header">
        <h1>사용자 관리</h1>
        <p className="user-count">총 {users.length}명</p>
      </div>

      <div className="users-table">
        <table>
          <thead>
            <tr>
              <th>프로필</th>
              <th>이름</th>
              <th>이메일</th>
              <th>가입일</th>
              <th>상태</th>
              <th>권한</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>
                  {user.picture ? (
                    <img
                      src={user.picture}
                      alt={user.name}
                      className="user-avatar"
                    />
                  ) : (
                    <div className="user-avatar-placeholder">
                      {user.name.charAt(0)}
                    </div>
                  )}
                </td>
                <td>
                  <strong>{user.name}</strong>
                </td>
                <td>{user.email}</td>
                <td className="date-cell">{formatDate(user.created_at)}</td>
                <td>
                  <span
                    className={`status-badge ${
                      user.is_active ? 'active' : 'inactive'
                    }`}
                  >
                    {user.is_active ? '활성' : '비활성'}
                  </span>
                </td>
                <td>
                  <span
                    className={`role-badge ${
                      user.is_admin ? 'admin' : 'user'
                    }`}
                  >
                    {user.is_admin ? '관리자' : '사용자'}
                  </span>
                </td>
                <td>
                  <div className="action-buttons">
                    <button
                      onClick={() =>
                        handleToggleAdmin(user.id, user.is_admin)
                      }
                      className={`btn-sm ${
                        user.is_admin ? 'btn-warning' : 'btn-primary'
                      }`}
                    >
                      {user.is_admin ? '권한 해제' : '관리자 지정'}
                    </button>
                    <button
                      onClick={() =>
                        handleToggleActive(user.id, user.is_active)
                      }
                      className={`btn-sm ${
                        user.is_active ? 'btn-danger' : 'btn-success'
                      }`}
                    >
                      {user.is_active ? '비활성화' : '활성화'}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default AdminUsers
