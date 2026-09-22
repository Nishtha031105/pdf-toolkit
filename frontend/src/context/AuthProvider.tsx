import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { getCurrentUser, loginUser, registerUser } from '../services/auth'
import { tokenStorage } from '../services/api'
import type { User } from '../types/api'

interface AuthValue { user: User | null; loading: boolean; login: (u: string, p: string) => Promise<void>; register: (u: string, p: string) => Promise<void>; logout: () => void }
const AuthContext = createContext<AuthValue | null>(null)
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(() => tokenStorage.get() !== null)
  useEffect(() => {
    if (!tokenStorage.get()) return
    getCurrentUser().then(setUser).catch(() => { tokenStorage.clear(); setUser(null) }).finally(() => setLoading(false))
  }, [])
  async function login(username: string, password: string) { const result = await loginUser(username, password); tokenStorage.set(result.access_token); setUser(result.user) }
  async function register(username: string, password: string) { const result = await registerUser(username, password); tokenStorage.set(result.access_token); setUser(result.user) }
  function logout() { tokenStorage.clear(); setUser(null) }
  return <AuthContext.Provider value={{ user, loading, login, register, logout }}>{children}</AuthContext.Provider>
}
export function useAuth() { const value = useContext(AuthContext); if (!value) throw new Error('useAuth must be used inside AuthProvider'); return value }
