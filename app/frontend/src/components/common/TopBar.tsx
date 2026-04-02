import { useState } from 'react'
import { documentApi } from '../../services/documentApi'
import { useDocumentStore } from '../../stores/documentStore'
import { useUIStore } from '../../stores/uiStore'

export function TopBar() {
  const title = useDocumentStore((s) => s.title)
  const setDocument = useDocumentStore((s) => s.setDocument)
  const setError = useUIStore((s) => s.setError)
  const setLoading = useUIStore((s) => s.setLoading)
  const [filePath, setFilePath] = useState('')

  const load = async () => {
    if (!filePath.trim()) return
    setLoading(true)
    setError(undefined)
    try {
      const doc = await documentApi.load(filePath.trim())
      setDocument({ id: doc.id, title: doc.title, blocks: doc.blocks || [] })
    } catch (error) {
      setError(error instanceof Error ? error.message : '加载文档失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <header style={{ padding: '10px 14px', borderBottom: '1px solid #ddd' }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>PaperClarity · {title || '未加载论文'}</div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          value={filePath}
          onChange={(event) => setFilePath(event.target.value)}
          placeholder="输入服务器可访问的 PDF 路径，例如 /workspace/PaperClarity_V2/xxx.pdf"
          style={{ flex: 1, padding: '6px 8px', border: '1px solid #ccc' }}
        />
        <button onClick={load} style={{ padding: '6px 10px' }}>
          加载论文
        </button>
      </div>
    </header>
  )
}
