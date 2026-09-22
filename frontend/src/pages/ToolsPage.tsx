import { useState } from 'react'
import { imagesToPdf, mergePdfs, splitPdf, getPagePreviews, shufflePdf } from '../services/tools'
import type { PageSizeOption, SplitMode } from '../types/api'

type Tool = 'images' | 'merge' | 'split' | 'shuffle'
function download(blob: Blob, name: string) { const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = name; link.click(); URL.revokeObjectURL(url) }
function FilePicker({ multiple, accept, files, onChange }: { multiple?: boolean; accept: string; files: File[]; onChange: (files: File[]) => void }) {
  return <label className="dropzone"><strong>{multiple ? 'Choose files' : 'Choose a file'}</strong><span className="muted">{files.length ? files.map((file) => file.name).join(', ') : `Accepted: ${accept}`}</span><input hidden type="file" accept={accept} multiple={multiple} onChange={(event) => onChange(Array.from(event.target.files ?? []))} /></label>
}
export default function ToolsPage({ tool }: { tool: Tool }) {
  const [files, setFiles] = useState<File[]>([]); const [busy, setBusy] = useState(false); const [message, setMessage] = useState(''); const [error, setError] = useState(''); const [size, setSize] = useState<PageSizeOption>('a4'); const [ranges, setRanges] = useState(''); const [mode, setMode] = useState<SplitMode>('ranges'); const [order, setOrder] = useState<number[]>([])
  async function run() {
    setBusy(true); setError(''); setMessage('')
    try {
      if (tool === 'images') { const result = await imagesToPdf(files, size); download(result.blob, result.filename); setMessage('Images converted and downloaded.') }
      if (tool === 'merge') { const result = await mergePdfs(files); download(result.blob, result.filename); setMessage('PDFs merged and downloaded.') }
      if (tool === 'split' && files[0]) { const result = await splitPdf(files[0], ranges, mode); download(result.blob, result.filename); setMessage('Split file downloaded.') }
      if (tool === 'shuffle' && files[0]) { const result = await shufflePdf(files[0], order.length ? order : Array.from({ length: 1 }, (_, i) => i + 1)); download(result.blob, result.filename); setMessage('Reordered PDF downloaded.') }
    } catch (err) { setError(err instanceof Error ? err.message : 'Operation failed.') } finally { setBusy(false) }
  }
  async function loadShuffle(selected: File[]) { setFiles(selected); setError(''); if (!selected[0]) return; try { const preview = await getPagePreviews(selected[0]); setOrder(Array.from({ length: preview.page_count }, (_, i) => i + 1)); setMessage(`${preview.page_count} pages loaded. Enter the new order below.`) } catch (err) { setError(err instanceof Error ? err.message : 'Could not read PDF.') } }
  const titles = { images: 'Images to PDF', merge: 'Merge PDF', split: 'Split PDF', shuffle: 'Shuffle PDF pages' }; const descriptions = { images: 'Select multiple JPG or PNG images, then create one PDF.', merge: 'Select two or more PDFs. All selected files will be merged in this order.', split: 'Select pages or ranges to extract from a PDF.', shuffle: 'Select a PDF, then enter every page number in its new order.' }
  const multiple = tool === 'images' || tool === 'merge'; const accept = multiple && tool === 'images' ? '.jpg,.jpeg,.png' : '.pdf'
  return <section className="card stack"><h1>{titles[tool]}</h1><p className="muted">{descriptions[tool]}</p><FilePicker multiple={multiple} accept={accept} files={files} onChange={tool === 'shuffle' ? loadShuffle : setFiles} />
    {tool === 'images' && files.length > 0 && <label className="field">Page size<select className="input" value={size} onChange={(e) => setSize(e.target.value as PageSizeOption)}><option value="a4">A4 with margins</option><option value="fit">Match image shape</option></select></label>}
    {tool === 'split' && files.length > 0 && <><label className="field">Pages or ranges<input className="input" value={ranges} placeholder="1-3, 5" onChange={(e) => setRanges(e.target.value)} /></label><label className="field">Output<select className="input" value={mode} onChange={(e) => setMode(e.target.value as SplitMode)}><option value="ranges">One PDF per range</option><option value="pages">One PDF per page</option></select></label></>}
    {tool === 'shuffle' && files.length > 0 && <label className="field">New page order<input className="input" value={order.join(',')} onChange={(e) => setOrder(e.target.value.split(',').filter(Boolean).map(Number))} placeholder="3,1,2" /></label>}
    <button className="btn" disabled={busy || !files.length || (multiple && files.length < 2)} onClick={run}>{busy ? 'Working...' : 'Process and download'}</button>{message && <p className="success-text">{message}</p>}{error && <p className="error-text">{error}</p>}
  </section>
}
