import { create } from 'zustand'

type Note = {
  id: number
  title: string
  content: string
}

type NoteState = {
  notes: Note[]
  setNotes: (notes: Note[]) => void
}

export const useNoteStore = create<NoteState>((set) => ({
  notes: [],
  setNotes: (notes) => set(() => ({ notes }))
}))
