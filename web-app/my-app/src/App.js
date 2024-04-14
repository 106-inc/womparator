import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    fetch('http://localhost:8080/api/hello')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setGreeting(data.message);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-title">{greeting}</h1>
      </header>
    </div>
  );
}

export default App;
