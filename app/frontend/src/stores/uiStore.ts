import { create } from 'zustand'

type UIState = {
  loading: boolean
  error?: string
  setLoading: (loading: boolean) => void
  setError: (error?: string) => void
}

export const useUIStore = create<UIState>((set) => ({
  loading: false,
  error: undefined,
  setLoading: (loading) => set(() => ({ loading })),
  setError: (error) => set(() => ({ error }))
}))
