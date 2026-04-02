import { useDocumentStore } from '../../stores/documentStore'
import { useSkillStore } from '../../stores/skillStore'

export function BottomStatusBar() {
  const page = useDocumentStore((s) => s.currentPage)
  const blockIds = useDocumentStore((s) => s.selectedBlockIds)
  const running = useSkillStore((s) => s.running)
  return (
    <footer style={{ padding: '8px 12px', borderTop: '1px solid #ddd', fontSize: 12, color: '#555' }}>
      当前页: {page} | 选中块: {blockIds.length} | Skill状态: {running ? '运行中' : '空闲'}
    </footer>
  )
}
