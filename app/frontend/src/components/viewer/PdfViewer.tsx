import { useDocumentStore } from '../../stores/documentStore'
import { EmptyState } from '../common/EmptyState'

export function PdfViewer() {
  const blocks = useDocumentStore((s) => s.blocks)
  const setSelection = useDocumentStore((s) => s.setSelection)

  if (!blocks.length) return <EmptyState text="请先通过后端接口加载 PDF。" />

  return (
    <div style={{ padding: 12, overflowY: 'auto', height: '100%' }}>
      {blocks.slice(0, 50).map((block) => (
        <p
          key={block.id}
          onClick={() => setSelection(block.text, [block.id])}
          style={{ cursor: 'pointer', lineHeight: 1.5, padding: '4px 0' }}
          title={`点击选择 block ${block.id}`}
        >
          {block.text}
        </p>
      ))}
    </div>
  )
}
