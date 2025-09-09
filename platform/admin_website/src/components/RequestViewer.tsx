import { FC } from 'react';
import { paths } from '../api/schema';

type RequestHistoryFileListResponse =
    paths['/get_request_history_file_list']['get']['responses']['200']['content']['application/json'];
type FileInfo = RequestHistoryFileListResponse['files'][number];

interface RequestViewerProps {
    fileInfo: FileInfo | null;
}

function formatDate(dateStr: string) {
    const match = dateStr.match(/^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})/);
    if (!match) return dateStr;
    const [, , month, day, hour, minute] = match;
    return `${day}/${month} ${hour}:${minute}`;
}

const RequestViewer: FC<RequestViewerProps> = ({ fileInfo }) => (
    <div>
        <h2>Détails</h2>
        {fileInfo ? (
            <div>
                <div><strong>Nom du fichier :</strong> {fileInfo.file_name}</div>
                <div><strong>Nom de la requête :</strong> {fileInfo.request_name}</div>
                <div><strong>Date de création :</strong> {formatDate(fileInfo.created_at)}</div>
            </div>
        ) : (
            <div>Sélectionne une requête à gauche</div>
        )}
    </div>
);

export default RequestViewer;