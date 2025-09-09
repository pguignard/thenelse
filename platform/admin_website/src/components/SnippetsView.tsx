import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchNdjsonSnippetsFileList, FileListResponse } from '../api/requests';

function SnippetsView() {
    const [selectedFile, setSelectedFile] = useState<string | null>(null);
    const { data, isLoading, isError } = useQuery<FileListResponse>({
        queryKey: ['ndjsonSnippetsFiles'],
        queryFn: fetchNdjsonSnippetsFileList,
    });

    return (
        <div style={{ display: 'flex', minHeight: '400px', border: '1px solid #eee' }}>
            {/* Liste à gauche */}
            <div style={{ flex: 1, borderRight: '1px solid #ddd', padding: '1rem', textAlign: 'left' }}>
                <h2>Database JSON</h2>
                {isLoading && <div>Chargement...</div>}
                {isError && <div>Erreur lors du chargement</div>}
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {data?.files.map((file) => (
                        <li key={file}>
                            <button
                                className={`filelist-button${selectedFile === file ? ' selected' : ''}`}
                                onClick={() => setSelectedFile(file)}
                            >
                                {file}
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
            {/* Détail à droite */}
            <div style={{ flex: 2, padding: '1rem', textAlign: 'left' }}>
                <h2>Détails</h2>
                {selectedFile ? (
                    <div>
                        <strong>Nom du fichier :</strong> {selectedFile}
                        {/* Tu pourras afficher le contenu du fichier ici plus tard */}
                    </div>
                ) : (
                    <div>Sélectionne un fichier à gauche</div>
                )}
            </div>
        </div>
    );
}

export default SnippetsView;