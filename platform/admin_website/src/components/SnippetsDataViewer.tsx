import { useState } from "react";

interface SnippetsDataViewerProps {
  responseContent: string;
}

const VIEW_MODES = [
  { key: "raw", label: "Raw json" },
  { key: "snippets", label: "Snippets" },
] as const;
type ViewMode = (typeof VIEW_MODES)[number]["key"];

type SnippetBatchDetails = {
  snippet_count: number;
  language: string;
  level: string;
  theme: string;
};

type Snippet = {
  snippet: string;
  choices: string[];
  answer_id: number;
  explanation: string;
};

function formatLLMResponseForTextArea(response_content: string | "") {
  // Formatte le JSON pour une meilleure lisibilité
  let formattedContent =
    response_content || "Impossible d’afficher le contenu.";
  try {
    formattedContent = JSON.stringify(JSON.parse(response_content), null, 2);
  } catch {
    // Si ce n'est pas un JSON valide, on laisse tel quel
  }
  return formattedContent;
}

function parseSnippetBatch(response_content: string | "") {
  // Parse le json, prend le premier élément et retourn ses détails :
  // language, level, theme
  let details: SnippetBatchDetails | null = null;
  try {
    const snippetArray = JSON.parse(response_content).snippets;
    if (Array.isArray(snippetArray) && snippetArray.length > 0) {
      const firstItem = snippetArray[0];
      details = {
        snippet_count: snippetArray.length,
        language: firstItem.language || "unknown",
        level: firstItem.level || "unknown",
        theme: firstItem.theme || "unknown",
      };
      console.log("Parsed batch details:", details);
    }
  } catch {
    console.log("Failed to parse batch details from response content.");
  }
  return details;
}

function createSnippetListFromResponse(response_content: string | "") {
  // Essaie de parser le JSON pour créer la liste des snippets
  let snippetList: Snippet[] = [];
  try {
    const snippetArray = JSON.parse(response_content).snippets;
    if (Array.isArray(snippetArray)) {
      snippetList = snippetArray.map((item) => ({
        snippet: item.snippet || "",
        choices: item.choices || [],
        answer_id: item.answer_id || 0,
        explanation: item.explanation || "",
      }));
    }
  } catch {
    console.log("Failed to parse snippet list from response content.");
  }
  return snippetList;
}

export function SnippetsDataViewer({
  responseContent,
}: SnippetsDataViewerProps) {
  const [mode, setMode] = useState<ViewMode>("snippets");
  const snippetList = createSnippetListFromResponse(responseContent);
  const batchDetails = parseSnippetBatch(responseContent);
  // Définit le mode par défaut en fonction du contenu

  return (
    <div>
      <div style={{ marginBottom: "1rem" }}>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value as ViewMode)}
          className="button selector"
        >
          {VIEW_MODES.map(({ key, label }) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>
      {mode === "raw" && (
        <textarea
          value={formatLLMResponseForTextArea(responseContent)}
          readOnly
          className="monospace-textarea"
        />
      )}
      {mode === "snippets" && snippetList && Array.isArray(snippetList) && (
        <div>
          {" "}
          {batchDetails && (
            <div style={{ marginBottom: "1rem" }}>
              <strong>Détails du batch :</strong>
              <br />
              Nombre de snippets : {batchDetails.snippet_count}
              <br />
              Langage : {batchDetails.language}
              <br />
              Niveau : {batchDetails.level}
              <br />
              Thème : {batchDetails.theme}
            </div>
          )}
          <div>
            {snippetList.map((item, index) => (
              <div
                key={index}
                style={{
                  marginBottom: "2rem",
                  padding: "1rem",
                  border: "1px solid #ccc",
                  borderRadius: "5px",
                }}
              >
                <div style={{ marginBottom: "0.5rem" }}>
                  <strong>Snippet {index + 1}:</strong>
                  <br />
                  <pre className="snippet-pre">{item.snippet}</pre>
                </div>
                <div style={{ marginBottom: "0.5rem" }}>
                  <strong>Choices:</strong>
                  <ul>
                    {item.choices.map((choice, cIndex) => (
                      <pre className="snippet-pre" key={cIndex}>
                        {choice}
                      </pre>
                    ))}
                  </ul>
                </div>
                <div style={{ marginBottom: "0.5rem" }}>
                  <strong>Answer ID:</strong> {item.answer_id}
                </div>
                <div>
                  <strong>Explanation:</strong>
                  <br />
                  <pre className="snippet-pre">{item.explanation}</pre>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      {mode === "snippets" && (!snippetList || !Array.isArray(snippetList)) && (
        <div>
          Impossible d’afficher les snippets (le contenu n’est pas un tableau
          JSON valide).
        </div>
      )}
    </div>
  );
}

export default SnippetsDataViewer;
