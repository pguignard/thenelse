import { useEffect, useState } from 'react';
import { useRequestHistoryFolderList, useRequestHistoryFolderContent } from '../api/hooks';
import { FolderInfo } from '../api/requests';
import RequestViewer from './RequestViewer';

interface RequestReportsProps {
    initialFolder?: string;
}

const DEFAULT_FOLDER = 'test';

function RequestReports({ initialFolder }: RequestReportsProps) {
    const [selectedFolder, setSelectedFolder] = useState<string>(initialFolder || DEFAULT_FOLDER);
    const [selectedFile, setSelectedFile] = useState<string | null>(null);

    // Utilisation des hooks centralisés
    const { data: foldersData, isLoading: isFoldersLoading } = useRequestHistoryFolderList();
    const { data: folderContentData, isLoading: isFilesLoading } = useRequestHistoryFolderContent(selectedFolder);

    // Reset du fichier sélectionné si le dossier change
    useEffect(() => {
        setSelectedFile(null);
    }, [selectedFolder]);

    // foldersData est maintenant un tableau de FolderInfo
    const folders: FolderInfo[] = foldersData?.folders ?? [];

    return (
        <div style={{ display: 'flex', minHeight: '400px', border: '1px solid #eee' }}>
            {/* Colonne gauche : Sélecteur de dossier + liste des fichiers */}
            <div style={{ flex: 1, borderRight: '1px solid #ddd', padding: '1rem', textAlign: 'left' }}>
                <h2>Requêtes LLM</h2>
                {/* Sélecteur de dossier */}
                {isFoldersLoading ? (
                    <div>Chargement des dossiers...</div>
                ) : (
                    <select
                        value={selectedFolder}
                        onChange={e => setSelectedFolder(e.target.value)}
                        className="button selector"
                    >
                        {folders.map(folder => (
                            <option key={folder.folder_name} value={folder.folder_name}>
                                {folder.folder_name}
                            </option>
                        ))}
                    </select>
                )}

                {/* Liste des fichiers */}
                {isFilesLoading && <div>Chargement des fichiers...</div>}
                <ul className="filelist">
                    {folderContentData?.files_infos.map((file) => (
                        <li key={file.file_name}>
                            <button
                                className={`button${selectedFile === file.file_name ? ' selected' : ''}`}
                                onClick={() => setSelectedFile(file.file_name)}
                            >
                                {file.request_name || file.file_name}
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
            {/* Colonne droite : Détail */}
            <div style={{ flex: 2, padding: '1rem', textAlign: 'left' }}>
                {selectedFile && (
                    <RequestViewer
                        fileName={selectedFile}
                        folderName={selectedFolder}
                    />
                )}
            </div>
        </div>
    );
}

export default RequestReports;