import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LegalDocumentApp from './components/LegalDocumentApp';
import UltraLegalSearchApp from './components/ultra-scale/UltraLegalSearchApp';
import './App.css';

function App() {
  return (
    <div className="App">
      <Routes>
        {/* Ultra-Scale Legal Research Application */}
        <Route path="/ultra-search" element={<UltraLegalSearchApp />} />
        
        {/* Original Legal Document Application */}
        <Route path="/legal-search" element={<LegalDocumentApp />} />
        
        {/* Default route - redirect to ultra-scale app */}
        <Route path="/" element={<Navigate to="/ultra-search" replace />} />
        
        {/* Catch-all route */}
        <Route path="*" element={<Navigate to="/ultra-search" replace />} />
      </Routes>
    </div>
  );
}

export default App;