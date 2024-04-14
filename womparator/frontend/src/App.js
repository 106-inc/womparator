import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [greeting, setGreeting] = useState('');

  function showFile() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
         var preview = document.getElementById('show-text');
         var file = document.querySelector('input[type=file]').files[0];
         var reader = new FileReader()

         var textFile = /text.*/;

         if (file.type.match(textFile)) {
            reader.onload = function (event) {
               let body = event.target.result;
               fetch('http://localhost:8080/upload', {
                method: 'POST',
                body,
              }).then((response) => {
                response.json().then((body) => {
                  console.log(response)
                })
                .catch(error => {
                  console.error('failed to post file:', error);
                });
              });
            }
         } else {
            preview.innerHTML = "<span class='error'>It doesn't seem to be a text file!</span>";
         }
         reader.readAsText(file);

   } else {
      alert("Your browser is too old to support HTML5 File API");
   }
  }

  useEffect(() => {
    fetch('http://localhost:8080/api/hello')
      .then(response => {
        console.log(response);
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
    <input type="file" onChange={showFile}/>
    <div id="show-text">Choose text File</div>
    </div>
  );
}

export default App;
