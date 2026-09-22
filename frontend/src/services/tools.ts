import { apiPostForm, apiPostFormForFile } from './api'
import type { DownloadedFile, PagePreviews, PdfInfo, SplitMode, PageSizeOption } from '../types/api'
export function imagesToPdf(files: File[], size: PageSizeOption): Promise<DownloadedFile> { const form = new FormData(); files.forEach((file) => form.append('files', file)); form.append('page_size', size); return apiPostFormForFile('/tools/images-to-pdf', form, 'images.pdf') }
export function mergePdfs(files: File[]): Promise<DownloadedFile> { const form = new FormData(); files.forEach((file) => form.append('files', file)); return apiPostFormForFile('/tools/merge-pdf', form, 'merged.pdf') }
export function getPdfInfo(file: File): Promise<PdfInfo> { const form = new FormData(); form.append('file', file); return apiPostForm('/tools/split-pdf/info', form) }
export function splitPdf(file: File, ranges: string, mode: SplitMode): Promise<DownloadedFile> { const form = new FormData(); form.append('file', file); form.append('ranges', ranges); form.append('mode', mode); return apiPostFormForFile('/tools/split-pdf', form, 'split.zip') }
export function getPagePreviews(file: File): Promise<PagePreviews> { const form = new FormData(); form.append('file', file); return apiPostForm('/tools/shuffle-pdf/preview', form) }
export function shufflePdf(file: File, order: number[]): Promise<DownloadedFile> { const form = new FormData(); form.append('file', file); form.append('order', order.join(',')); return apiPostFormForFile('/tools/shuffle-pdf', form, 'shuffled.pdf') }
