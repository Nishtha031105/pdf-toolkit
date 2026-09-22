import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import AuthCard from '../components/AuthCard'
import { useAuth } from '../context/AuthProvider'

interface AuthPageProps { onAuthenticated?: (token: string) => void }

export default function AuthPage({ onAuthenticated }: AuthPageProps) {
  const auth = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [mode, setMode] = useState<'login' | 'register'>(location.pathname === '/register' ? 'register' : 'login')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (auth.loading) return <div className="center-screen muted">Loading...</div>
  if (auth.user) return <Navigate to="/" replace />

  async function handleSubmit(username: string, password: string) {
    setLoading(true)
    setError('')

    try {
      if (mode === 'login') {
        await auth.login(username, password)
        onAuthenticated?.('')
      } else {
        await auth.register(username, password)
      }
      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="stack">
      <div className="tab-row">
        <button
          className={mode === 'login' ? 'tab active' : 'tab'}
          onClick={() => { setMode('login'); navigate('/login') }}
        >
          Login
        </button>
        <button
          className={mode === 'register' ? 'tab active' : 'tab'}
          onClick={() => { setMode('register'); navigate('/register') }}
        >
          Register
        </button>
      </div>

      <AuthCard
        title={mode === 'login' ? 'Login' : 'Register'}
        submitLabel={mode === 'login' ? 'Log in' : 'Create account'}
        onSubmit={handleSubmit}
        loading={loading}
        error={error}
      />
    </div>
  )
}
