import { noteApi } from '../../services/noteApi'
import { useDocumentStore } from '../../stores/documentStore'
import { useNoteStore } from '../../stores/noteStore'
import { useSkillStore } from '../../stores/skillStore'

export function SaveToNoteButton() {
  const documentId = useDocumentStore((s) => s.documentId)
  const output = useSkillStore((s) => s.output)
  const setNotes = useNoteStore((s) => s.setNotes)

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
