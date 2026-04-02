import { useSkillStore } from '../../stores/skillStore'

export function SkillTabs() {
  const { skills, currentSkill, setCurrentSkill } = useSkillStore()
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, padding: 8, borderBottom: '1px solid #eee' }}>
      {skills.map((skill) => (
        <button
          key={skill.name}
          onClick={() => setCurrentSkill(skill)}
          style={{
            border: '1px solid #ddd',
            background: currentSkill?.name === skill.name ? '#eef' : '#fff',
            padding: '4px 8px'
          }}
        >
          {skill.display_name}
        </button>
      ))}
    </div>
  )
}
