import { useDocumentStore } from '../../stores/documentStore'

export function ContextBar() {
  const selectedText = useDocumentStore((s) => s.selectedText)
  return <div style={{ padding: 8, fontSize: 12, color: '#555' }}>上下文: {selectedText ? '段落选择' : '整篇论文'}</div>
}
