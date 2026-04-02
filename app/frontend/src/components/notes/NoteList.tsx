import { useEffect } from 'react'
import { noteApi } from '../../services/noteApi'
import { useDocumentStore } from '../../stores/documentStore'

import { useNoteStore } from '../../stores/noteStore'

export function NoteList() {
  const notes = useNoteStore((s) => s.notes)
  const setNotes = useNoteStore((s) => s.setNotes)
  const documentId = useDocumentStore((s) => s.documentId)

  useEffect(() => {
    if (!documentId) {
      setNotes([])
      return
    }
    noteApi.list(documentId).then((items) => setNotes(items as any)).catch(() => undefined)
  }, [documentId, setNotes])

  return (
    <div style={{ padding: 8, borderTop: '1px solid #eee' }}>
      <strong>笔记</strong>
      <ul>
        {notes.map((note) => (
          <li key={note.id}>{note.title}</li>
        ))}
      </ul>
    </div>
  )
}
