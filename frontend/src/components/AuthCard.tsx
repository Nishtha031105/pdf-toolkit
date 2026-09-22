import { useState } from 'react'

interface AuthCardProps {
  onSubmit: (username: string, password: string) => Promise<void>
  submitLabel: string
  title: string
  loading: boolean
  error?: string
}

export default function AuthCard({
  onSubmit,
  submitLabel,
  title,
  loading,
  error,
}: AuthCardProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await onSubmit(username, password)
  }

  return (
    <section className="card auth-card">
      <h2>{title}</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>

        {error && <p className="error-text">{error}</p>}

        <button className="btn" type="submit" disabled={loading}>
          {loading ? 'Please wait...' : submitLabel}
        </button>
      </form>
    </section>
  )
}
