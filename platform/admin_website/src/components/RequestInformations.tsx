import { components } from '../api/schema';

type CostInformations = components['schemas']['CostInformations'];
type LLMResponse = components['schemas']['LLMResponse'];

export function RequestInformations({
    cost,
    llm,
}: {
    cost: CostInformations;
    llm: LLMResponse;
}) {
    const totalTokens = (llm.input_tokens ?? 0) + (llm.output_tokens ?? 0) + (llm.reasoning_tokens ?? 0);

    return (
        <div>
            <div style={{ fontSize: '1rem', fontWeight: 'bold', marginBottom: '1rem' }}>
                Prix total: {cost.total_cost.toFixed(5)} cent <br />
                Tokens: {totalTokens}
            </div>
            <table style={{ width: '60%', borderCollapse: 'collapse', marginBottom: '1.5rem' }}>
                <thead>
                    <tr>
                        <th></th>
                        <th>Prix (cent)</th>
                        <th>Tokens</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Input</td>
                        <td>{cost.input_cost.toFixed(5)}</td>
                        <td>{llm.input_tokens}</td>
                    </tr>
                    <tr>
                        <td>Output</td>
                        <td>{cost.output_cost.toFixed(5)}</td>
                        <td>{llm.output_tokens}</td>
                    </tr>
                    <tr>
                        <td>Reasoning</td>
                        <td>{cost.reasoning_cost.toFixed(5)}</td>
                        <td>{llm.reasoning_tokens}</td>
                    </tr>
                </tbody>
            </table>
            <div style={{ fontSize: '1rem', color: '#666', marginBottom: '0.5rem' }}>
                <strong>Modèle :</strong> {llm.model}<br />
                <strong>Température :</strong> {llm.temperature}<br />
                <strong>Service tier :</strong> {llm.service_tier}<br />
                <strong>Raisonnement :</strong> {cost.reasoning_percent}% du prix total
            </div>
        </div>
    );
}