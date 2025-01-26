import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home'; // Import the Home page component
import Simulations from './pages/Simulations'; // Import the About page component
import './App.css';

function App() {
  return (
    <Router>
      <nav className="navbar">
        <div className="logo">Algo Tester</div>
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link> {/* Link to the Home page */}
          <Link to="/Simulations" className="nav-link">Simulations</Link> {/* Link to the About page */}
        </div>
      </nav>
      {/* Navigation Bar */}
      
      
      <Routes>
        <Route path="/" element={<Home />} /> {/* Home page route */}
        <Route path="/Simulations" element={<Simulations />} /> {/* About page route */}
      </Routes>
    </Router>
  );
}

export default App;
