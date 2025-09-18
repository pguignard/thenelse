import { paths, components } from './schema';

const baseUrl = 'http://localhost:8000'; // À adapter selon l'environnement

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

// 2. /get_request_history_folder_list (GET)
export type FolderInfo = components['schemas']['FolderInfo'];
export type RHFolderListResponse =
    paths['/get_request_history_folder_list']['get']['responses']['200']['content']['application/json'];

export async function fetchRequestHistoryFolderList(): Promise<RHFolderListResponse> {
    return fetchUrl<RHFolderListResponse>('/get_request_history_folder_list');
}

// 3. /get_request_history_folder_content (GET)
export type RHFolderContentResponse =
    paths['/get_request_history_folder_content']['get']['responses']['200']['content']['application/json'];

export async function fetchRequestHistoryFolderContent(folderName: string): Promise<RHFolderContentResponse> {
    const url = `/get_request_history_folder_content?folder_name=${encodeURIComponent(folderName)}`;
    return fetchUrl<RHFolderContentResponse>(url);
}

// 4. /get_request_information (GET)
export type RequestInformationsResponse =
    paths['/get_request_information']['get']['responses']['200']['content']['application/json'];

export async function fetchRequestInformation(fileName: string, folderName: string): Promise<RequestInformationsResponse> {
    const url = `/get_request_information?file_name=${encodeURIComponent(fileName)}&folder_name=${encodeURIComponent(folderName)}`;
    return fetchUrl<RequestInformationsResponse>(url);
}
