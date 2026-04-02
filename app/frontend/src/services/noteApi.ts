import { apiRequest } from './api'

export type NoteDTO = {
  id: number
  title: string
  content: string
}

export const noteApi = {
  create(payload: { document_id: string; title: string; content: string; citations: unknown[] }) {
    return apiRequest<NoteDTO>('/notes', { method: 'POST', body: JSON.stringify(payload) })
  },
  list(documentId: string) {
    return apiRequest<NoteDTO[]>(`/notes/${documentId}`)
  }
}
