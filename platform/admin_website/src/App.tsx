import { useState } from 'react';
import RequestReports from './components/RequestReports';
import MultiRequest from './components/MultiRequest';
import './App.css';

function App() {
  const [activePage, setActivePage] = useState<'request_reports' | 'multi_request'>('request_reports');

  return (
    <div className="app">
      <h1>⚙️ Admin website</h1>
      <header>
        <button className={`button header-button${activePage === 'request_reports' ? ' selected' : ''}`} onClick={() => setActivePage('request_reports')}>📊 Request reports</button>
        <button className={`button header-button${activePage === 'multi_request' ? ' selected' : ''}`} onClick={() => setActivePage('multi_request')}>🚀 Multi Request</button>
      </header>
      <main>
        {activePage === 'request_reports' ? <RequestReports /> : <MultiRequest />}
      </main>
    </div>
  );
}

export default App;
