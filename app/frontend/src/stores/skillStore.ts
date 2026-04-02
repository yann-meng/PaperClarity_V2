import { create } from 'zustand'
import type { SkillInfo, SkillOutput } from '../types'

type SkillState = {
  skills: SkillInfo[]
  currentSkill?: SkillInfo
  running: boolean
  output?: SkillOutput
  setSkills: (skills: SkillInfo[]) => void
  setCurrentSkill: (skill: SkillInfo) => void
  setRunning: (running: boolean) => void
  setOutput: (output: SkillOutput) => void
}

export const useSkillStore = create<SkillState>((set) => ({
  skills: [],
  running: false,
  setSkills: (skills) => set(() => ({ skills, currentSkill: skills[0] })),
  setCurrentSkill: (skill) => set(() => ({ currentSkill: skill })),
  setRunning: (running) => set(() => ({ running })),
  setOutput: (output) => set(() => ({ output }))
}))
