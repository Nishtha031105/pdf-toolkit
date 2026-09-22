import { Link, useNavigate } from 'react-router-dom'
import type { ReactNode } from 'react'
import { useAuth } from '../context/AuthProvider'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="container">
          <Link className="app-logo" to="/">PDF Toolkit</Link>
          <nav className="app-nav"><Link to="/images-to-pdf">Images to PDF</Link><Link to="/merge-pdf">Merge PDF</Link><Link to="/split-pdf">Split PDF</Link><Link to="/shuffle-pdf">Shuffle pages</Link></nav>
          <span className="muted">{user?.username}</span><button className="btn btn--ghost" onClick={() => { logout(); navigate('/login') }}>Log out</button>
        </div>
      </header>
      <main className="container app-main">{children}</main>
    </div>
  )
}
