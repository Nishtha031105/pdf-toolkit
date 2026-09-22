import { useState } from 'react'
import PdfToolCard from '../components/PdfToolCard'

const API_BASE = '/api'

export default function PdfToolsPage() {
  const [result, setResult] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function readPdfInfo(file: File) {
    setLoading(true)
    setError('')
    setResult('')

    try {
      const form = new FormData()
      form.append('file', file)

      const response = await fetch(`${API_BASE}/pdf/info`, {
        method: 'POST',
        body: form,
      })

      if (!response.ok) {
        throw new Error('Unable to read PDF metadata.')
      }

      const data = await response.json()
      setResult(`Pages: ${data.page_count} | Title: ${data.title}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'PDF info failed.')
    } finally {
      setLoading(false)
    }
  }

  async function mergePdfs(fileList: File[]) {
    if (fileList.length < 2) {
      setError('Select at least two PDF files to merge.')
      return
    }

    setLoading(true)
    setError('')
    setResult('')

    try {
      const form = new FormData()
      fileList.forEach((file) => form.append('files', file))

      const response = await fetch(`${API_BASE}/pdf/merge`, {
        method: 'POST',
        body: form,
      })

      if (!response.ok) {
        throw new Error('Merge failed.')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'merged.pdf'
      link.click()
      URL.revokeObjectURL(url)
      setResult('Merged PDF downloaded.')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Merge failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="stack">
      <PdfToolCard
        title="PDF info"
        description="Read page count and document metadata from a PDF."
        onSubmit={readPdfInfo}
        buttonLabel="Inspect PDF"
        accept="application/pdf"
        loading={loading}
      />

      <PdfToolCard
        title="Merge PDFs"
        description="Select multiple PDFs and download the combined result."
        onSubmit={async (file) => {
          const target = (document.getElementById('merge-files') as HTMLInputElement | null)?.files
          const files = target ? Array.from(target) : [file]
          await mergePdfs(files)
        }}
        buttonLabel="Merge selected"
        accept="application/pdf"
        loading={loading}
      />

      <input id="merge-files" type="file" accept="application/pdf" multiple style={{ display: 'none' }} />

      {result && <p className="success-text">{result}</p>}
      {error && <p className="error-text">{error}</p>}
    </div>
  )
}
