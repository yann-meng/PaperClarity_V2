import { useSkillStore } from '../../stores/skillStore'
import { EmptyState } from '../common/EmptyState'

export function OutputPanel() {
  const output = useSkillStore((s) => s.output)
  if (!output) return <EmptyState text="运行技能后在此显示结构化输出。" />

  return (
    <div style={{ padding: 12, overflowY: 'auto', height: '100%' }}>
      <h3>{output.title}</h3>
      <p>{output.summary}</p>
      {output.sections?.map((section, idx) => (
        <section key={idx}>
          <h4>{section.label}</h4>
          <p>{section.content}</p>
        </section>
      ))}
    </div>
  )
}
