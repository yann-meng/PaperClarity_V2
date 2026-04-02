import { apiRequest } from './api'
import type { SkillInfo, SkillOutput } from '../types'

export const skillApi = {
  list() {
    return apiRequest<SkillInfo[]>('/skills')
  },
  run(skillName: string, payload: Record<string, unknown>) {
    return apiRequest<SkillOutput>(`/skills/${skillName}/run`, {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  }
}
