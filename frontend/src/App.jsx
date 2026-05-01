import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ApartmentList from './pages/ApartmentList.jsx';
import ApartmentPage from './pages/ApartmentPage.jsx';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<ApartmentList />} />
          <Route path="/apartment/:id" element={<ApartmentPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
