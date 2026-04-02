import { exportApi } from '../../services/exportApi'
import { useDocumentStore } from '../../stores/documentStore'
import { useUIStore } from '../../stores/uiStore'

function downloadText(filename: string, text: string) {
  const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}

export function ExportMarkdownButton() {
  const documentId = useDocumentStore((s) => s.documentId)
  const title = useDocumentStore((s) => s.title)
  const setError = useUIStore((s) => s.setError)
  const setLoading = useUIStore((s) => s.setLoading)

  const exportMarkdown = async () => {
    if (!documentId) return
    setLoading(true)
    setError(undefined)
    try {
      const { markdown } = await exportApi.markdown(documentId)
      const filename = `${title || 'paper'}-notes.md`
      downloadText(filename, markdown)
    } catch (error) {
      setError(error instanceof Error ? error.message : '导出失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <button onClick={exportMarkdown} style={{ margin: 8, padding: '6px 10px' }}>
      导出 Markdown
    </button>
  )
}
