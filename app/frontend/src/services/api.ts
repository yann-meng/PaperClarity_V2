const BASE_URL = 'http://localhost:8000/api'

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
    ...init
  })
  const payload = await response.json()
  if (!response.ok || payload.success === false) {
    throw new Error(payload.detail || payload.error || 'Request failed')
  }
  return payload.data as T
}
