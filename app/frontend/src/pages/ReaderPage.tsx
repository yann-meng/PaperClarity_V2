import { useEffect } from 'react'
import { ContextBar } from '../components/assistant/ContextBar'
import { OutputPanel } from '../components/assistant/OutputPanel'
import { PromptPreview } from '../components/assistant/PromptPreview'
import { RunSkillButton } from '../components/assistant/RunSkillButton'
import { SkillTabs } from '../components/assistant/SkillTabs'
import { EmptyState } from '../components/common/EmptyState'
import { ErrorBanner } from '../components/common/ErrorBanner'
import { Loading } from '../components/common/Loading'
import { NoteList } from '../components/notes/NoteList'
import { SaveToNoteButton } from '../components/notes/SaveToNoteButton'
import { ModelSettingsPanel } from '../components/settings/ModelSettingsPanel'
import { OutlinePanel } from '../components/viewer/OutlinePanel'
import { PageNavigator } from '../components/viewer/PageNavigator'
import { PdfViewer } from '../components/viewer/PdfViewer'
import { TextSelectionOverlay } from '../components/viewer/TextSelectionOverlay'
import { skillApi } from '../services/skillApi'
import { useSkillStore } from '../stores/skillStore'
import { useUIStore } from '../stores/uiStore'

export function ReaderPage({ side }: { side: 'left' | 'right' }) {
  const setSkills = useSkillStore((s) => s.setSkills)
  const error = useUIStore((s) => s.error)
  const loading = useUIStore((s) => s.loading)

  useEffect(() => {
    skillApi.list().then(setSkills).catch(() => undefined)
  }, [setSkills])

  if (side === 'left') {
    return (
      <section style={{ borderRight: '1px solid #ddd', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <OutlinePanel />
        <PageNavigator />
        <TextSelectionOverlay />
        <div style={{ flex: 1, minHeight: 0 }}>
          <PdfViewer />
        </div>
      </section>
    )
  }

  return (
    <section style={{ minWidth: 0, display: 'flex', flexDirection: 'column' }}>
      <SkillTabs />
      <ContextBar />
      {error ? <ErrorBanner message={error} /> : null}
      {loading ? <Loading /> : null}
      <div style={{ flex: 1, minHeight: 0 }}>
        <OutputPanel />
      </div>
      <RunSkillButton />
      <SaveToNoteButton />
      <ModelSettingsPanel />
      <NoteList />
      <PromptPreview />
      <EmptyState text="可继续补充：Prompt 编辑、引用回跳、多模型切换。" />
    </section>
  )
}
