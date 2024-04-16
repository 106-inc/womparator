import React, { useState, useEffect } from 'react';
import { Box } from '@mui/system';
import './App.css';

function Item(props) {
  const { sx, ...other } = props;
  return (
    <Box
      sx={{
        p: 1,
        m: 1,
        ...sx,
      }}
      {...other}
    />
  );
}


function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDisabled, setIsDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [buttonText, setButtonText] = useState('Select your files first');

  const Form = () => (
    <form>
      <label className='uploader'>
        <div className='upload-space'>
          <>
            {preview ? (
              <div className='preview'>
                <img
                  src={preview}
                  alt='Preview of the file to be uploaded'
                />
              </div>
            ) : (
              <i className='icon-upload'></i>
            )}
            <input type='file' onChange={onFileSelected} />
          </>
        </div>
        <p className='filename'>
          {fileName ? fileName : 'No file selected yet'}
        </p>
      </label>
    </form>
  );

  // Handling file selection from input
  const onFileSelected = (e) => {
    if (e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setFileName(e.target.files[0].name);
      setIsDisabled(false); // Enabling upload button
      setButtonText("Let's upload this!");
    }
  };

  // Setting image preview
  useEffect(() => {
    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(selectedFile);
    }
  }, [selectedFile]);

  // Setting image preview
  useEffect(() => {
    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(selectedFile);
    }
  }, [selectedFile]);

  return (
    <div className='app'>
      <header className='title'>
        <h1>Compare documents</h1>
      </header>
      <main>
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'nowrap',
          }}
        >
          <Item><Form /></Item>
          <Item><Form /></Item>
        </Box>
        <Box sx={{
          display: 'flex',
          flexWrap: 'nowrap',
          justifyContent: 'flex-end'
        }}>
          <Item sx={{ gridRow: '1', gridColumn: '4 / 5' }}>
            <button
              type='submit'
              className='btn'
              disabled={isDisabled}
              tabIndex={0}
            >
              {buttonText}
            </button></Item>
        </Box>
      </main>
    </div>
  );
}

export default App;
