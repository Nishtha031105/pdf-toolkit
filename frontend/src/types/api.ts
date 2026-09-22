export interface User { id: number; username: string }
export interface TokenResponse { access_token: string; token_type: string; user: User }
export interface PdfInfo { filename: string; page_count: number }
export interface PagePreviews { page_count: number; pages: string[] }
export interface DownloadedFile { blob: Blob; filename: string }
export type PageSizeOption = 'a4' | 'fit'
export type SplitMode = 'ranges' | 'pages'
export interface HealthResponse { status: string; service: string; pymupdf_version: string; pillow_version: string }
