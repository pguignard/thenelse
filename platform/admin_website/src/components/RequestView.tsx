import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { paths } from '../api/schema';
import { fetchRequestHistoryFileList } from '../api/requests';
import RequestViewer from './RequestViewer';

type RequestHistoryFileListResponse =
    paths['/get_request_history_file_list']['get']['responses']['200']['content']['application/json'];

type FileInfo = RequestHistoryFileListResponse['files'][number];

function formatDate(dateStr: string) {
    const match = dateStr.match(/^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})/);
    if (!match) return dateStr;
    const [, , month, day, hour, minute] = match;
    return `${day}/${month} ${hour}:${minute}`;
}
function RequestTitle(file: FileInfo | null) {
    if (!file) return "Sélectionne une requête à gauche";
    return `${file.request_name} - ${formatDate(file.created_at)}`;
}

function RequestView() {
    const [selectedFile, setSelectedFile] = useState<FileInfo | null>(null);
    const { data, isLoading, isError } = useQuery<RequestHistoryFileListResponse>({
        queryKey: ['requestHistoryFilesInfos'],
        queryFn: fetchRequestHistoryFileList,
    });

    const sortedFiles = data?.files
        ?.slice()
        .sort((a, b) => b.created_at.localeCompare(a.created_at));

    return (
        <div style={{ display: 'flex', minHeight: '400px', border: '1px solid #eee' }}>
            {/* Liste à gauche */}
            <div style={{ flex: 1, borderRight: '1px solid #ddd', padding: '1rem', textAlign: 'left' }}>
                <h2>Requêtes LLM</h2>
                {isLoading && <div>Chargement...</div>}
                {isError && <div>Erreur lors du chargement</div>}
                <ul className="filelist">
                    {sortedFiles?.map((file) => (
                        <li key={file.file_name}>
                            <button
                                className={`filelist-button${selectedFile?.file_name === file.file_name ? ' selected' : ''}`}
                                onClick={() => setSelectedFile(file)}
                            >
                                <div className="filelist-request-name">{file.request_name}</div>
                                <div className="filelist-date">{formatDate(file.created_at)}</div>
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
            {/* Détail à droite */}
            <div style={{ flex: 2, padding: '1rem', textAlign: 'left' }}>
                <h2>{RequestTitle(selectedFile) || 'Détails de la requête'}</h2>
                {selectedFile && <RequestViewer fileName={selectedFile.file_name} />}
            </div>
        </div>
    );
}

export default RequestView;