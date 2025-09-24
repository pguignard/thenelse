import { useState } from "react";
import {
  useRequestHistoryFolderList,
  useRequestHistoryFolderContent,
} from "../api/hooks";
import { FolderInfo } from "../api/requests";

const DEFAULT_FOLDER = "old";

function MultiRequest() {
  const [selectedFolder, setSelectedFolder] = useState<string>(DEFAULT_FOLDER);

  // Liste des dossiers
  const { data: foldersData, isLoading: isFoldersLoading } =
    useRequestHistoryFolderList();
  // Infos du dossier sélectionné
  const { data: folderContentData, isLoading: isFolderLoading } =
    useRequestHistoryFolderContent(selectedFolder);

  const folders: FolderInfo[] = foldersData?.folders ?? [];

  return (
    <div
      style={{ display: "flex", minHeight: "400px", border: "1px solid #eee" }}
    >
      {/* Colonne gauche : liste des dossiers */}
      <div className="filelist-container">
        <h2>Dossiers multi-requêtes</h2>
        {isFoldersLoading ? (
          <div>Chargement des dossiers...</div>
        ) : (
          <ul className="filelist">
            {folders.map((folder) => (
              <li key={folder.folder_name}>
                <button
                  className={`button${
                    selectedFolder === folder.folder_name ? " selected" : ""
                  }`}
                  onClick={() => setSelectedFolder(folder.folder_name)}
                >
                  {folder.folder_name}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
      {/* Colonne droite : infos du dossier sélectionné */}
      <div className="right-panel">
        {isFolderLoading && <div>Chargement du dossier...</div>}
        {folderContentData && folderContentData.folder_info && (
          <div>
            <h2>{selectedFolder}</h2>
            <div
              style={{
                fontSize: "1.3rem",
                fontWeight: "bold",
                marginBottom: "1rem",
              }}
            >
              {folderContentData.folder_info.files_count} fichiers &nbsp;-&nbsp;
              {folderContentData.folder_info.total_cost.toFixed(4)} cents
            </div>
            <div style={{ marginBottom: "1rem" }}>
              <strong>Fichiers invalides :</strong>{" "}
              {folderContentData.folder_info.invalid_files_count}
            </div>
            <div style={{ marginBottom: "1rem" }}>
              <strong>Modèles utilisés :</strong>{" "}
              {folderContentData.folder_info.models.join(", ")}
            </div>
            <div style={{ marginBottom: "1rem" }}>
              <strong>Input tokens :</strong>{" "}
              {folderContentData.folder_info.input_tokens} &nbsp;|&nbsp;
              <strong>Output tokens :</strong>{" "}
              {folderContentData.folder_info.output_tokens}
            </div>
            <div style={{ marginBottom: "1rem" }}>
              <strong>Input cost :</strong>{" "}
              {folderContentData.folder_info.input_cost.toFixed(5)} cents
              &nbsp;|&nbsp;
              <strong>Output cost :</strong>{" "}
              {folderContentData.folder_info.output_cost.toFixed(5)} cents
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MultiRequest;
