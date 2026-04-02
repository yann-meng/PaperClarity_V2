import { apiRequest } from './api'

export const settingsApi = {
  getLLMSettings() {
    return apiRequest<{ llm_provider: string; llm_base_url: string; llm_model: string }>('/settings/llm')
  }
}
