import { apiPostJson, apiRequest } from './api'
import type { TokenResponse, User } from '../types/api'

export function registerUser(username: string, password: string): Promise<TokenResponse> { return apiPostJson('/auth/register', { username, password }) }

export function loginUser(username: string, password: string): Promise<TokenResponse> { return apiPostJson('/auth/login', { username, password }) }

export function getCurrentUser(): Promise<User> { return apiRequest<User>('/auth/me') }
