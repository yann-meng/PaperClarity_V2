import { noteApi } from '../../services/noteApi'
import { useDocumentStore } from '../../stores/documentStore'
import { useNoteStore } from '../../stores/noteStore'
import { useSkillStore } from '../../stores/skillStore'
import { useUIStore } from '../../stores/uiStore'

export function SaveToNoteButton() {
  const documentId = useDocumentStore((s) => s.documentId)
  const output = useSkillStore((s) => s.output)
  const setNotes = useNoteStore((s) => s.setNotes)
  const setError = useUIStore((s) => s.setError)

  const save = async () => {
    if (!documentId || !output) return
    try {
      await noteApi.create({
        document_id: documentId,
        title: output.title,
        content: output.raw_text || output.summary,
        citations: output.citations || []
      })
      const notes = await noteApi.list(documentId)
      setNotes(notes)
    } catch (error) {
      setError(error instanceof Error ? error.message : '保存笔记失败')
    }

  const save = async () => {
    if (!documentId || !output) return
    await noteApi.create({
      document_id: documentId,
      title: output.title,
      content: output.raw_text || output.summary,
      citations: output.citations || []
    })
    const notes = (await noteApi.list(documentId)) as any[]
    setNotes(notes as any)

  }

  return (
    <button onClick={save} style={{ margin: 8, padding: '6px 10px' }}>
      保存到笔记
    </button>
  )
}
