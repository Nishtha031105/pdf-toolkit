import { useEffect, useState } from 'react'
import { getHealth } from '../services/health'
import type { HealthResponse } from '../types/api'

type HealthState =
  | { status: 'loading' }
  | { status: 'ok'; data: HealthResponse }
  | { status: 'error'; message: string }

export default function HomePage() {
  const [state, setState] = useState<HealthState>({ status: 'loading' })
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let cancelled = false

    getHealth()
      .then((data) => {
        if (!cancelled) setState({ status: 'ok', data })
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setState({
            status: 'error',
            message: err instanceof Error ? err.message : 'Something went wrong.',
          })
        }
      })

    return () => {
      cancelled = true
    }
  }, [attempt])

  function retry() {
    setState({ status: 'loading' })
    setAttempt((n) => n + 1)
  }

  return (
    <section className="card">
      <h1>Backend connection</h1>

      {state.status === 'loading' && <p className="muted">Checking backend…</p>}

      {state.status === 'ok' && (
        <>
          <p>
            <span className="badge badge--success">Connected</span>
          </p>
          <dl className="info-list">
            <dt>Service</dt>
            <dd>{state.data.service}</dd>
            <dt>PyMuPDF</dt>
            <dd>{state.data.pymupdf_version}</dd>
            <dt>Pillow</dt>
            <dd>{state.data.pillow_version}</dd>
          </dl>
        </>
      )}

      {state.status === 'error' && (
        <>
          <p>
            <span className="badge badge--danger">Disconnected</span>
          </p>
          <p className="muted">{state.message}</p>
          <button className="btn" onClick={retry}>
            Retry
          </button>
        </>
      )}
    </section>
  )
}
