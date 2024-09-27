import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import TrackDetail from './pages/TrackDetail';
import GlobalAudioPlayer from './components/AudioPlayer';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tracks/:id" element={<TrackDetail />} />
        </Routes>
        <GlobalAudioPlayer />
      </div>
    </Router>
  );
}

export default App;