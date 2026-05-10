import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ApartmentList from './pages/ApartmentList.jsx';
import ApartmentPage from './pages/ApartmentPage.jsx';
import './App.css';
import Analytics from './pages/Analytics.jsx';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<ApartmentList />} />
          <Route path="/apartment/:id" element={<ApartmentPage />} />
          <Route path="/analytics" element = {<Analytics/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
