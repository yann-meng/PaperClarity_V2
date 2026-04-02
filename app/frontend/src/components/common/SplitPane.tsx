import type { PropsWithChildren } from 'react'

export function SplitPane({ children }: PropsWithChildren) {
  return <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', flex: 1, minHeight: 0 }}>{children}</div>
}
