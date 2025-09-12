import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchRequestInformation } from '../api/requests';
import { paths, components } from '../api/schema';
import { RequestInformations } from './RequestInformations';
import { SnippetsDataViewer } from './SnippetsDataViewer';

type RequestInformationResponse =
    paths['/get_request_information']['get']['responses']['200']['content']['application/json'];

interface RequestViewerProps {
    fileName: string | null;
}

const VIEW_LABELS = [
    { key: 'request_informations', label: 'Infos requête' },
    { key: 'prompt', label: 'Prompt' },
    { key: 'response_content', label: 'Réponse LLM' },
] as const;
type ViewKey = typeof VIEW_LABELS[number]['key'];

type CostInformations = components['schemas']['CostInformations'];
type LLMResponse = components['schemas']['LLMResponse'];


function RequestViewer({ fileName }: RequestViewerProps) {
    const [activeView, setActiveView] = useState<ViewKey>('request_informations');

    const { data, isLoading, isError } = useQuery<RequestInformationResponse>({
        queryKey: ['requestInformation', fileName],
        queryFn: () => fetchRequestInformation(fileName as string),
        enabled: !!fileName,
    });


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
                    {activeView === 'request_informations' && data && (
                        <RequestInformations cost={data.cost_info} llm={data.llm_response} />
                    )}
                    {activeView === 'prompt' && (
                        <textarea
                            value={data.prompt || ''}
                            readOnly
                            className="monospace-textarea"
                        />
                    )}
                    {activeView === 'response_content' && data && (
                        <SnippetsDataViewer responseContent={data.response_content || ''} />
                    )}
                </div>
            )}
        </div>
    );
}

export default RequestViewer;