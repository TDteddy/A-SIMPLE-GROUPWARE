import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import PostList from './pages/PostList'
import PostDetail from './pages/PostDetail'
import PostCreate from './pages/PostCreate'
import PostEdit from './pages/PostEdit'
import AdminDashboard from './pages/AdminDashboard'
import AdminUsers from './pages/AdminUsers'
import AdminPosts from './pages/AdminPosts'
import './App.css'

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return user ? children : <Navigate to="/login" />
}

function App() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            >
              <Route index element={<Navigate to="/posts" replace />} />
              <Route path="posts" element={<PostList />} />
              <Route path="posts/:id" element={<PostDetail />} />
              <Route path="posts/new" element={<PostCreate />} />
              <Route path="posts/:id/edit" element={<PostEdit />} />
            </Route>
            <Route
              path="/admin"
              element={
                <PrivateRoute>
                  <AdminDashboard />
                </PrivateRoute>
              }
            >
              <Route path="users" element={<AdminUsers />} />
              <Route path="posts" element={<AdminPosts />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </GoogleOAuthProvider>
  )
}

export default App
