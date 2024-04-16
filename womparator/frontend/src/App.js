import React, { useState, useEffect } from 'react';
import { Box } from '@mui/system';
import GoogleDocPreview from './assets/fonts/GoogleDocsIcon.svg'
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
  const [files] = useState(new Map());
  const [filenames] = useState(new Map());
  const [fileContents] = useState(new Map());
  const [DescrPreview, setDescPreview] = useState(false);
  const [ReqPreview, setReqPreview] = useState(false);
  const [dummyEvent, setDummy] = useState(null);
  const [isDisabled, setIsDisabled] = useState(true);
  const [buttonText, setButtonText] = useState('Select your files first');

  const FormType = {
    Description: 'Description',
    Requirements: 'Requirements',
  };

  // Handling file selection from input
  const onFileSelected = (e, formType) => {
    let file = e.target.files[0];
    if (file) {
      files.set(formType, file);
      filenames.set(formType, file.name);
      if (files.size > 1) {
        setIsDisabled(false); // Enabling upload button
        setButtonText("Compare!");
      }
    }
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        switch (formType) {
          case FormType.Description:
            setDescPreview(true);
            break;
          case FormType.Requirements:
            setReqPreview(true);
            break;
        }
      };
      reader.onload = () => fileContents.set(formType, reader.result)
      reader.readAsText(file);
    }
  };

  const onCompareButton = () => {
    const body = {
      "Description": fileContents.get(FormType.Description),
      "Requirements": fileContents.get(FormType.Requirements),
    };
    fetch('http://localhost:8080/upload', {
      method: 'POST',
      body: JSON.stringify(body),
    }).then((response) => {
      response.json().then((body) => {
        console.log(response)
      })
        .catch(error => {
          console.error('failed to post file:', error);
        });
    });
  }

  function Form(props) {
    let filename = filenames.get(props.type);
    let preview = false;
    switch (props.type) {
      case FormType.Description:
        preview = DescrPreview;
        break;
      case FormType.Requirements:
        preview = ReqPreview;
        break;
    }
    return (<form>
      <label className='uploader'>
        <div className='upload-space'>
          <>
            {preview ? (
              <div className='preview'>
                <img
                  src={GoogleDocPreview}
                  alt='Preview of the file to be uploaded'
                />
              </div>
            ) : (
              <i className='icon-upload'></i>
            )}
            <input type='file' onChange={(e) => onFileSelected(e, props.type)} />
          </>
        </div>
        <p className='filename'>
          {filename ? filename : 'No file selected yet'}
        </p>
      </label>
    </form>);
  }

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
          <Item><Form type={FormType.Description}/></Item>
          <Item><Form type={FormType.Requirements}/></Item>
        </Box>
        <Box sx={{
          display: 'flex',
          flexWrap: 'nowrap',
          justifyContent: 'flex-end'
        }}>
          <Item>
            <button
              type='submit'
              className='btn'
              disabled={isDisabled}
              tabIndex={0}
              onClick={onCompareButton}
            >
              {buttonText}
            </button></Item>
        </Box>
      </main>
    </div>
  );
}

export default App;
