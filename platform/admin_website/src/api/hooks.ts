import { useQuery } from '@tanstack/react-query';
import {
    fetchHealth,
    fetchRequestHistoryFolderList,
    fetchRequestHistoryFolderContent,
    fetchRequestInformation,
    HealthResponse,
    RHFolderListResponse,
    RHFolderContentResponse,
    RequestInformationsResponse,
} from './requests';

// Hook pour /health
export function useHealth() {
    return useQuery<HealthResponse>({
        queryKey: ['health'],
        queryFn: fetchHealth,
    });
}

// Hook pour la liste des dossiers
export function useRequestHistoryFolderList() {
    return useQuery<RHFolderListResponse>({
        queryKey: ['requestHistoryFolderList'],
        queryFn: fetchRequestHistoryFolderList,
    });
}

// Hook pour le contenu d'un dossier
export function useRequestHistoryFolderContent(folderName: string) {
    return useQuery<RHFolderContentResponse>({
        queryKey: ['requestHistoryFolderContent', folderName],
        queryFn: () => fetchRequestHistoryFolderContent(folderName),
        enabled: !!folderName,
    });
}

// Hook pour les infos d'un fichier dans un dossier
export function useRequestInformation(fileName: string | null, folderName: string | null) {
    return useQuery<RequestInformationsResponse>({
        queryKey: ['requestInformation', fileName, folderName],
        queryFn: () => fetchRequestInformation(fileName as string, folderName as string),
        enabled: !!fileName && !!folderName,
    });
}