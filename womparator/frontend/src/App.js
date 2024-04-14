import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDisabled, setIsDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [buttonText, setButtonText] = useState('Select your file first');

  const Spinner = () => (
    <svg
      className='spinner'
      width='65px'
      height='65px'
      viewBox='0 0 66 66'
      xmlns='http://www.w3.org/2000/svg'
    >
      <circle
        className='path'
        fill='none'
        strokeWidth='6'
        strokeLinecap='round'
        cx='33'
        cy='33'
        r='30'
      ></circle>
    </svg>
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

  const handleFileUpload = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setIsDisabled(true);
    setButtonText("Wait we're uploading your file...");

    try {
      if (selectedFile !== '') {

        fetch('http://localhost:8080/upload', {
          method: 'POST',
          body: selectedFile,
        }).then((response) => {
          response.json().then((body) => {
            console.log(response)
          })
          .catch(error => {
            console.error('failed to post file:', error);
          });
        });
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className='app'>
      <header className='title'>
        <h1>Text compare</h1>
      </header>
      <main>
        <form onSubmit={(e) => handleFileUpload(e)}>
        <label className='uploader'>
            <div className='upload-space'>
              {isLoading ? (
                <Spinner />
              ) : (
                <>
                  {isError || isSuccess ? (
                    <i
                      className={`icon-${isSuccess ? 'success' : 'error'}`}
                    ></i>
                  ) : (
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
                  )}
                </>
              )}
            </div>
            {isError || isSuccess ? (
              <p className={isSuccess ? 'success' : 'error'}>
                {isSuccess ? 'Upload successful!' : 'Something went wrong ...'}
              </p>
            ) : (
              <p className='filename'>
                {fileName ? fileName : 'No file selected yet'}
              </p>
            )}
          </label>
          <button
            type='submit'
            className='btn'
            disabled={isDisabled}
            tabIndex={0}
          >
            {buttonText}
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
