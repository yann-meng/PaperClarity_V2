export type Block = {
  id: string
  page: number
  section_id?: string | null
  block_type: string
  text: string
  order: number
}

export type SkillInfo = {
  name: string
  display_name: string
  description: string
  supported_contexts: string[]
}

export type SkillOutput = {
  title: string
  summary: string
  sections: { label: string; content: string }[]
  citations: { page: number; block_id: string }[]
  raw_text: string
}
