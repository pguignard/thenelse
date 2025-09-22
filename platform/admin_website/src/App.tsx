import { useState } from "react";
import RequestReports from "./components/RequestReports";
import MultiRequest from "./components/MultiRequest";
import "./App.css";

function App() {
  enum Page {
    RequestReports = "request_reports",
    MultiRequest = "multi_request",
  }
  const [activePage, setActivePage] = useState<Page>(Page.RequestReports);

  return (
    <div className="app">
      <h1>⚙️ Admin website</h1>
      <header>
        <button
          className={`button header-button${
            activePage === Page.RequestReports ? " selected" : ""
          }`}
          onClick={() => setActivePage(Page.RequestReports)}
        >
          📊 Request reports
        </button>
        <button
          className={`button header-button${
            activePage === Page.MultiRequest ? " selected" : ""
          }`}
          onClick={() => setActivePage(Page.MultiRequest)}
        >
          📊 Multi Request
        </button>
      </header>
      <main>
        {activePage === Page.RequestReports ? (
          <RequestReports />
        ) : (
          <MultiRequest />
        )}
      </main>
    </div>
  );
}

export default App;
