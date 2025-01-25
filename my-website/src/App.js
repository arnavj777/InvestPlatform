import React, { useEffect, useState } from 'react';
import './App.css'

function App() {
  const symbol_sumbit = () => {
    console.log("Input Value", symbol_input)
  }
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/data')
      .then(response => response.json())
      .then(data => setMessage(data.message));
  }, []);

  return (
    <div style={{ width: "100%", height: "100vh", backgroundColor: "#151B24", display: "flex", flexDirection: "column" }}>

    {/* Navigation Bar /}

        <nav style={{ width: "100%", height: "60px", backgroundColor: "#1A1E29", display: "flex", alignItems: "center", padding: "0px", boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.25)" }}>
        <div style={{ color: "#FFFFFF", fontSize: "20px", fontWeight: "bold", cursor: "pointer" }}>
          Logo
        </div>
        <div style={{ marginLeft: "auto", display: "flex", gap: "20px" }}>
          <a href="#" style={{ color: "#FFFFFF", textDecoration: "none", fontSize: "16px", fontWeight: "500", cursor: "pointer" }}>Home</a>
          <a href="#" style={{ color: "#FFFFFF", textDecoration: "none", fontSize: "16px", fontWeight: "500", cursor: "pointer" }}>About</a>
          <a href="#" style={{ color: "#FFFFFF", textDecoration: "none", fontSize: "16px", fontWeight: "500", cursor: "pointer" }}>Contact</a>
        </div>
        </nav>
        {/ Main Content */}

        <div style={{ width: "100%", height: "100vh", backgroundColor: "#0D1117", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <div style={{ width: "90%", height: "50%", backgroundColor: "#141820", marginBottom: "20px", borderRadius: "8px" }}></div>
          <div style={{ width: "90%", height: "30%", backgroundColor: "#2765c2", borderRadius: "8px" }}>
            
            <div>
              <label htmlFor='textInput'>
                Enter Stock Symbol
              </label>
              <input id="textInput" type="text" value={symbol_input}></input>
            </div>
            
          </div>
        </div>
      </div>



  );
}

export default App;