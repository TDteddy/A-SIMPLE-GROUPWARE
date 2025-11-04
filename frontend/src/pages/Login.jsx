import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { GoogleLogin } from '@react-oauth/google'
import { useAuth } from '../context/AuthContext'
import './Login.css'

function Login() {
  const navigate = useNavigate()
  const { user, login } = useAuth()

  useEffect(() => {
    if (user) {
      navigate('/')
    }
  }, [user, navigate])

  const handleSuccess = async (credentialResponse) => {
    try {
      await login(credentialResponse.credential)
      navigate('/')
    } catch (error) {
      console.error('Login error:', error)
      alert('로그인에 실패했습니다. BRYZE 이메일로 다시 시도해주세요.')
    }
  }

  const handleError = () => {
    console.error('Login Failed')
    alert('로그인에 실패했습니다.')
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>BRYZE Groupware</h1>
          <p>사내 게시판 및 그룹웨어</p>
        </div>
        <div className="login-content">
          <p className="login-instruction">
            BRYZE 구글 계정으로 로그인하세요
          </p>
          <div className="login-button-wrapper">
            <GoogleLogin
              onSuccess={handleSuccess}
              onError={handleError}
              useOneTap
              theme="filled_blue"
              size="large"
              text="signin_with"
              shape="rectangular"
            />
          </div>
        </div>
        <div className="login-footer">
          <p>© 2024 BRYZE. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}

export default Login
