import { paths } from './schema';

const baseUrl = 'http://localhost:8000'; // Peut être ajusté selon l'environnement

// Utilitaire générique pour fetcher et typer la réponse
export async function fetchUrl<T = any>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${baseUrl}${url}`, options);
    if (!response.ok) {
        throw new Error(`Erreur lors de la requête vers ${url}`);
    }
    return response.json();
}

// 1. /health (GET)
export type HealthResponse =
    paths['/health']['get']['responses']['200']['content']['application/json'];

export async function fetchHealth(): Promise<HealthResponse> {
    return fetchUrl<HealthResponse>('/health');
}

// 2. /get_request_history_file_list (GET)
export type RequestHistoryFileListResponse =
    paths['/get_request_history_file_list']['get']['responses']['200']['content']['application/json'];

export async function fetchRequestHistoryFileList(): Promise<RequestHistoryFileListResponse> {
    return fetchUrl<RequestHistoryFileListResponse>('/get_request_history_file_list');
}

// à voir plus tard

// 3. /get_request_information (GET)
export type RequestInformationsResponse =
    paths['/get_request_information']['get']['responses']['200']['content']['application/json'];

export async function fetchRequestInformation(file_name: string): Promise<RequestInformationsResponse> {
    const url = `/get_request_information?file_name=${encodeURIComponent(file_name)}`;
    return fetchUrl<RequestInformationsResponse>(url);
}
