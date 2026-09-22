import type { DownloadedFile } from '../types/api'

const API_BASE = '/api'
const TOKEN_KEY = 'pdf_toolkit_token'

export const tokenStorage = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function extractErrorMessage(response: Response): Promise<string> {
  try {
    const body = await response.json()
    if (typeof body?.detail === 'string') {
      return body.detail
    }
  } catch {
    // Response body was empty or not JSON.
  }

  if (response.status >= 500) {
    return 'The server is unavailable or ran into a problem. Please try again.'
  }

  return `Request failed (${response.status}).`
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers)
  const token = tokenStorage.get()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  let response: Response

  try {
    response = await fetch(`${API_BASE}${path}`, { ...init, headers })
  } catch {
    throw new ApiError('Cannot reach the server. Is the backend running?', 0)
  }

  if (!response.ok) {
    throw new ApiError(await extractErrorMessage(response), response.status)
  }

  return (await response.json()) as T
}

export function apiPostJson<T>(path: string, body: unknown) {
  return apiRequest<T>(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
}

export async function apiPostFormForFile(path: string, form: FormData, fallback: string): Promise<DownloadedFile> {
  const response = await apiRequestResponse(path, { method: 'POST', body: form })
  const disposition = response.headers.get('Content-Disposition') ?? ''
  const filename = /filename="?([^";]+)"?/i.exec(disposition)?.[1] ?? fallback
  return { blob: await response.blob(), filename }
}

export function apiPostForm<T>(path: string, form: FormData) {
  return apiRequest<T>(path, { method: 'POST', body: form })
}

async function apiRequestResponse(path: string, init: RequestInit): Promise<Response> {
  const headers = new Headers(init.headers)
  const token = tokenStorage.get()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers })
  if (!response.ok) {
    let message = `Request failed (${response.status}).`
    try { const body = await response.json(); if (typeof body.detail === 'string') message = body.detail } catch { /* empty response */ }
    throw new Error(message)
  }
  return response
}
