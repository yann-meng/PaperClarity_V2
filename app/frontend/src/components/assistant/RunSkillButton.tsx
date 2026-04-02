import { skillApi } from '../../services/skillApi'
import { useDocumentStore } from '../../stores/documentStore'
import { useSkillStore } from '../../stores/skillStore'
import { useUIStore } from '../../stores/uiStore'

export function RunSkillButton() {
  const { documentId, selectedBlockIds, selectedText } = useDocumentStore()
  const { currentSkill, setRunning, setOutput } = useSkillStore()
  const setError = useUIStore((s) => s.setError)

  const run = async () => {
    if (!currentSkill || !documentId) return
    setRunning(true)
    setError(undefined)
    try {
      const contextType = selectedText ? 'paragraph' : 'paper'
      const result = await skillApi.run(currentSkill.name, {
        document_id: documentId,
        context_type: contextType,
        selected_block_ids: selectedBlockIds
      })
      setOutput(result)
    } catch (error) {
      setError(error instanceof Error ? error.message : '运行失败')
    } finally {
      setRunning(false)
    }
  }

  return (
    <button onClick={run} style={{ margin: 8, padding: '6px 10px' }}>
      运行 Skill
    </button>
  )
}
