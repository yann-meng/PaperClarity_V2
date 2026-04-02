import { create } from 'zustand'
import type { Block } from '../types'

type DocumentState = {
  documentId: string
  title: string
  currentPage: number
  selectedText: string
  selectedBlockIds: string[]
  blocks: Block[]
  setDocument: (input: { id: string; title: string; blocks?: Block[] }) => void
  setSelection: (text: string, blockIds: string[]) => void
}

export const useDocumentStore = create<DocumentState>((set) => ({
  documentId: '',
  title: '',
  currentPage: 1,
  selectedText: '',
  selectedBlockIds: [],
  blocks: [],
  setDocument: (input) => set(() => ({ documentId: input.id, title: input.title, blocks: input.blocks || [] })),
  setSelection: (text, blockIds) => set(() => ({ selectedText: text, selectedBlockIds: blockIds }))
}))
