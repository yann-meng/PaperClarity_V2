import { BottomStatusBar } from '../components/common/BottomStatusBar'
import { TopBar } from '../components/common/TopBar'
import { SplitPane } from '../components/common/SplitPane'
import { ReaderPage } from '../pages/ReaderPage'

export function MainLayout() {
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <TopBar />
      <SplitPane>
        <ReaderPage side="left" />
        <ReaderPage side="right" />
      </SplitPane>
      <BottomStatusBar />
    </div>
  )
}
