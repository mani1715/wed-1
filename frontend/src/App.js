import { BrowserRouter, Routes, Route } from 'react-router-dom';
import InvitationViewer from './pages/InvitationViewer';
import DesignSelector from './pages/DesignSelector';
import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DesignSelector />} />
          <Route path="/invitation/:design" element={<InvitationViewer />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
