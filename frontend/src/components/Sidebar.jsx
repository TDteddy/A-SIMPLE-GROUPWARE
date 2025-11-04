import { NavLink } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <NavLink
          to="/posts"
          className={({ isActive }) =>
            isActive ? 'sidebar-link active' : 'sidebar-link'
          }
        >
          <span className="sidebar-icon">📋</span>
          게시판
        </NavLink>
        {/* 추가 메뉴는 여기에 추가할 수 있습니다 */}
      </nav>
    </aside>
  )
}

export default Sidebar
