import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        {/* Aquí puedes agregar otras rutas como Login, Dashboard, etc. */}
      </Routes>
    </Router>
  );
}

export default App;
