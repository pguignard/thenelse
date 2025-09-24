import { useEffect, useState } from "react";
import {
  useRequestHistoryFolderList,
  useRequestHistoryFolderContent,
} from "../api/hooks";
import { FolderInfo } from "../api/requests";
import RequestViewer from "./RequestViewer";

// Pour appeller la page avec un dossier spécifique (depuis MultiRequest)
interface RequestReportsProps {
  initialFolder?: string;
}

const DEFAULT_FOLDER = "old";

function formatDate(dateStr: string) {
  // Ex: "20250902_123045" → "02/09 12:30"
  const match = dateStr.match(/^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})/);
  if (!match) return dateStr;
  const [, year, month, day, hour, minute] = match;
  return `${day}/${month} ${hour}:${minute}`;
}

function truncate(str: string, n: number) {
  return str.length > n ? str.slice(0, n - 1) + "…" : str;
}

function RequestReports({ initialFolder }: RequestReportsProps) {
  const [selectedFolder, setSelectedFolder] = useState<string>(
    initialFolder || DEFAULT_FOLDER
  );
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  const { data: foldersData, isLoading: isFoldersLoading } =
    useRequestHistoryFolderList();
  const {
    data: folderContentData,
    isLoading: isFilesLoading,
    refetch: refetchFolderContent,
  } = useRequestHistoryFolderContent(selectedFolder);

  useEffect(() => {
    setSelectedFile(null);
  }, [selectedFolder]);

  const folders: FolderInfo[] = foldersData?.folders ?? [];

  // Tri des fichiers par date décroissante
  const sortedFiles =
    folderContentData?.files_infos
      ?.slice()
      .sort((a, b) => b.created_at.localeCompare(a.created_at)) ?? [];

  return (
    <div
      style={{ display: "flex", minHeight: "400px", border: "1px solid #eee" }}
    >
      {/* Colonne gauche : Sélecteur de dossier + liste des fichiers */}
      <div className="filelist-container">
        <h2>Requêtes LLM</h2>
        {/* Sélecteur de dossier + bouton refresh */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            marginBottom: "1rem",
          }}
        >
          {isFoldersLoading ? (
            <div>Chargement des dossiers...</div>
          ) : (
            <>
              <select
                value={selectedFolder}
                onChange={(e) => setSelectedFolder(e.target.value)}
                className="button selector"
              >
                {folders.map((folder) => (
                  <option key={folder.folder_name} value={folder.folder_name}>
                    {folder.folder_name}
                  </option>
                ))}
              </select>
              <button
                type="button"
                className="refresh-button"
                title="Rafraîchir la liste"
                onClick={() => refetchFolderContent()}
              >
                🔄
              </button>
            </>
          )}
        </div>

        {/* Liste des fichiers */}
        {isFilesLoading && <div>Chargement des fichiers...</div>}
        <ul className="filelist">
          {sortedFiles.map((file) => (
            <li key={file.file_name}>
              <button
                className={`button${
                  selectedFile === file.file_name ? " selected" : ""
                }`}
                onClick={() => setSelectedFile(file.file_name)}
              >
                <div
                  className="filelist-request-name"
                  title={file.request_name}
                >
                  {truncate(file.request_name, 30)}
                </div>
                <div className="filelist-date">
                  {formatDate(file.created_at)}
                </div>
              </button>
            </li>
          ))}
        </ul>
      </div>
      {/* Colonne droite : Détail */}
      <div className="right-panel">
        <h2>Détail de la requête</h2>
        {selectedFile ? (
          <RequestViewer fileName={selectedFile} folderName={selectedFolder} />
        ) : (
          <div>Aucun fichier sélectionné</div>
        )}
      </div>
    </div>
  );
}

export default RequestReports;
