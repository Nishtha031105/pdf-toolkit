import { useState } from 'react'

interface PdfToolCardProps {
  title: string
  description: string
  onSubmit: (file: File) => Promise<void>
  buttonLabel: string
  accept?: string
  loading?: boolean
  fileName?: string
}

export default function PdfToolCard({
  title,
  description,
  onSubmit,
  buttonLabel,
  accept,
  loading = false,
  fileName,
}: PdfToolCardProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  async function handleSubmit() {
    if (!selectedFile) return
    await onSubmit(selectedFile)
  }

  return (
    <section className="card pdf-card">
      <h2>{title}</h2>
      <p className="muted">{description}</p>
      <div className="tool-row">
        <input
          type="file"
          accept={accept}
          onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
        />
        <button className="btn" onClick={handleSubmit} disabled={!selectedFile || loading}>
          {loading ? 'Working...' : buttonLabel}
        </button>
      </div>
      {fileName && <p className="notice">Selected: {fileName}</p>}
    </section>
  )
}
