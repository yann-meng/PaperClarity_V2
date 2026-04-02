import { useDocumentStore } from '../../stores/documentStore'

export function TopBar() {
  const title = useDocumentStore((s) => s.title)
  return (
    <header style={{ padding: '10px 14px', borderBottom: '1px solid #ddd', fontWeight: 600 }}>
      PaperClarity · {title || '未加载论文'}
    </header>
  )
}
