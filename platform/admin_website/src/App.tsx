import { useState } from 'react';
import RequestReports from './components/RequestReports';
import RequestLauncher from './components/RequestLauncher';
import './App.css';

function App() {
  const [activePage, setActivePage] = useState<'request_reports' | 'request_launcher'>('request_reports');

  return (
    <div className="app">
      <h1>⚙️ Admin website</h1>
      <header>
        <button className={`button header-button${activePage === 'request_reports' ? ' selected' : ''}`} onClick={() => setActivePage('request_reports')}>📊 Request reports</button>
        <button className={`button header-button${activePage === 'request_launcher' ? ' selected' : ''}`} onClick={() => setActivePage('request_launcher')}>🚀 Request Launcher</button>
      </header>
      <main>
        {activePage === 'request_reports' ? <RequestReports /> : <RequestLauncher />}
      </main>
    </div>
  );
}

export default App;
