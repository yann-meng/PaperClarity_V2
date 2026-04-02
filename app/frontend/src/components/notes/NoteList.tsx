import { useNoteStore } from '../../stores/noteStore'

export function NoteList() {
  const notes = useNoteStore((s) => s.notes)
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
