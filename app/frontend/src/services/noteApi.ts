import { apiRequest } from './api'

export const noteApi = {
  create(payload: { document_id: string; title: string; content: string; citations: unknown[] }) {
    return apiRequest('/notes', { method: 'POST', body: JSON.stringify(payload) })
  },
  list(documentId: string) {
    return apiRequest(`/notes/${documentId}`)
  }
}
