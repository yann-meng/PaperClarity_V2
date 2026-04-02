import { apiRequest } from './api'
import type { Block } from '../types'

export const documentApi = {
  load(filePath: string) {
    return apiRequest<{ id: string; title: string; blocks: Block[] }>('/documents/load', {
      method: 'POST',
      body: JSON.stringify({ file_path: filePath })
    })
  },
  getBlocks(documentId: string) {
    return apiRequest<Block[]>(`/documents/${documentId}/blocks`)
  }
}
