import { useState } from 'react';
import RequestView from './components/RequestView';
import SnippetsView from './components/SnippetsView';
import './App.css';

function App() {
  const [activePage, setActivePage] = useState<'requests' | 'database'>('requests');

  return (
    <div className="app">
      <h1>Admin website</h1>
      <header>
        <button onClick={() => setActivePage('requests')}>Voir les requêtes</button>
        <button onClick={() => setActivePage('database')}>Voir la database JSON</button>
      </header>
      <main>
        {activePage === 'requests' ? <RequestView /> : <SnippetsView />}
      </main>
    </div>
  );
}

export default App;
