import config from '../config';

export interface UploadResponse {
    table_name: string;
    rows_loaded: number;
}

class IngestService {
    private baseUrl: string;

    constructor() {
        this.baseUrl = `${config.backendUrl}/ingest`;
    }

    async uploadFile(file: File): Promise<UploadResponse> {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseUrl}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();
            return data as UploadResponse;
        } catch (error) {
            if (error instanceof Error) {
                throw new Error(`File upload failed: ${error.message}`);
            }
            throw new Error('File upload failed');
        }
    }
}

export const ingestService = new IngestService();