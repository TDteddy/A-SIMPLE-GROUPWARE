import { useAuth } from '../context/AuthContext'
import { useNavigate, Link } from 'react-router-dom'
import './Header.css'

function Header() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1 className="header-title">BRYZE Groupware</h1>
        </div>
        <div className="header-right">
          {user && (
            <div className="user-info">
              {user.picture && (
                <img
                  src={user.picture}
                  alt={user.name}
                  className="user-avatar"
                />
              )}
              <span className="user-name">{user.name}</span>
              {user.is_admin && (
                <Link to="/admin" className="admin-button">
                  관리자
                </Link>
              )}
              <button onClick={handleLogout} className="logout-button">
                로그아웃
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
