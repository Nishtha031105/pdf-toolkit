import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import type { ReactNode } from 'react'
import Layout from './components/Layout'
import AuthPage from './pages/AuthPage'
import HomePage from './pages/HomePage'
import ToolsPage from './pages/ToolsPage'
import { AuthProvider, useAuth } from './context/AuthProvider'

function Protected({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="center-screen muted">Loading...</div>
  return user ? <>{children}</> : <Navigate to="/login" replace />
}

export default function App() {
  return <BrowserRouter><AuthProvider><Routes>
    <Route path="/login" element={<AuthPage />} />
    <Route path="/register" element={<AuthPage />} />
    <Route path="/" element={<Protected><Layout><HomePage /></Layout></Protected>} />
    <Route path="/images-to-pdf" element={<Protected><Layout><ToolsPage tool="images" /></Layout></Protected>} />
    <Route path="/merge-pdf" element={<Protected><Layout><ToolsPage tool="merge" /></Layout></Protected>} />
    <Route path="/split-pdf" element={<Protected><Layout><ToolsPage tool="split" /></Layout></Protected>} />
    <Route path="/shuffle-pdf" element={<Protected><Layout><ToolsPage tool="shuffle" /></Layout></Protected>} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes></AuthProvider></BrowserRouter>
}
