// Utilitaires pour interagir avec l'API backend

const BASE_URL = 'http://localhost:8000';

export async function fetchUrl<T = any>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${BASE_URL}${url}`, options);
    if (!response.ok) {
        throw new Error(`Erreur lors de la récupération de ${url}`);
    }
    return response.json();
}

// Récupère la liste des fichiers de l'historique des requêtes LLM avec leurs informations

export interface RequestFileInfo {
    file_name: string;
    request_name: string;
    created_at: string;
}

export interface RequestFileInfosResponse {
    files: RequestFileInfo[];
}

export async function fetchRequestHistoryFileInfos(): Promise<RequestFileInfosResponse> {
    const response = await fetchUrl<RequestFileInfosResponse>('/get_request_history_file_infos');
    return response;
}

// Récupère le contenu d'un fichier d'historique des requêtes LLM spécifique



// Ancien code, à garder pour référence

export interface FileListResponse {
    files: string[];
}

// Utilitaire pour fetcher une liste de fichiers
async function fetchFileList(url: string): Promise<FileListResponse> {
    const response = await fetch(`${BASE_URL}${url}`);
    if (!response.ok) {
        throw new Error('Erreur lors de la récupération des fichiers');
    }
    return response.json();
}
// Récupère la liste des fichiers NDJSON snippets
export function fetchNdjsonSnippetsFileList(): Promise<FileListResponse> {
    return fetchFileList('/get_ndjson_snippets_file_list');
}

