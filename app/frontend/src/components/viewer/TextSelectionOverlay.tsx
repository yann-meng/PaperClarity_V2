import { useDocumentStore } from '../../stores/documentStore'

export function TextSelectionOverlay() {
  const text = useDocumentStore((s) => s.selectedText)
  if (!text) return null
  return <div style={{ padding: 8, background: '#f8f8ff', fontSize: 12 }}>当前选中文本: {text.slice(0, 120)}</div>
}
