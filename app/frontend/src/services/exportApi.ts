import { apiRequest } from './api'

export const exportApi = {
  markdown(documentId: string) {
    return apiRequest<{ markdown: string }>('/export/markdown', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId })
    })
  }
}
