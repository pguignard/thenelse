import { useState } from 'react';
import { useRequestInformation } from '../api/hooks';
import { RequestInformationsResponse } from '../api/requests';
import { RequestInformations } from './RequestInformations';
import { SnippetsDataViewer } from './SnippetsDataViewer';

interface RequestViewerProps {
    fileName: string | null;
    folderName: string | null;
}

const VIEW_LABELS = [
    { key: 'request_informations', label: 'Infos requête' },
    { key: 'prompt', label: 'Prompt' },
    { key: 'response_content', label: 'Réponse LLM' },
] as const;
type ViewKey = typeof VIEW_LABELS[number]['key'];

function RequestViewer({ fileName, folderName }: RequestViewerProps) {
    const [activeView, setActiveView] = useState<ViewKey>('request_informations');

    const { data, isLoading, isError } = useRequestInformation(fileName, folderName);

    return (
        <div>
            <div style={{ display: 'flex', marginBottom: '2rem' }}>
                {VIEW_LABELS.map(({ key, label }) => (
                    <button
                        key={key}
                        onClick={() => setActiveView(key)}
                        className={`button${activeView === key ? ' selected' : ''}`}
                    >
                        {label}
                    </button>
                ))}
            </div>
            {isLoading && <div>Chargement...</div>}
            {isError && <div>Erreur lors du chargement</div>}
            {!fileName && <div>Sélectionne une requête à gauche</div>}
            {data && fileName && (
                <div>
                    {activeView === 'request_informations' && (
                        <RequestInformations cost={data.cost_info} llm={data.llm_response} />
                    )}
                    {activeView === 'prompt' && (
                        <textarea
                            value={data.prompt || ''}
                            readOnly
                            className="monospace-textarea"
                        />
                    )}
                    {activeView === 'response_content' && (
                        <SnippetsDataViewer responseContent={data.response_content || ''} />
                    )}
                </div>
            )}
        </div>
    );
}

export default RequestViewer;