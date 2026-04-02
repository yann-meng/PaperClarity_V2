export function ErrorBanner({ message }: { message: string }) {
  return <div style={{ background: '#fee', color: '#900', padding: 10, border: '1px solid #f99' }}>{message}</div>
}
