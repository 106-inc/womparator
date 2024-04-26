import React, { useState } from 'react';
import { Box } from '@mui/system';
import { useNavigate } from "react-router-dom";

import Particles from "react-tsparticles";
import { particlesOptions, particlesInit } from "./DynamicBack"

import GoogleDocPreview from './assets/fonts/GoogleDocsIcon.svg'

import { ReactComponent as GaspromLogo } from './assets/fonts/GaspromLogo.svg'
import { ReactComponent as TeamLogo } from './assets/fonts/TeamLogo.svg'
import { ReactComponent as MiptLogo } from './assets/fonts/MiptLogo.svg'

import './App.css';
import './Header.css'

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

export default function ImportFiles() {
  const [files] = useState(new Map());
  const [filenames] = useState(new Map());
  const [DescrPreview, setDescPreview] = useState(false);
  const [ReqPreview, setReqPreview] = useState(false);
  const [isDisabled, setIsDisabled] = useState(true);
  const [buttonText, setButtonText] = useState('Select your files first');

  const FormType = {
    Description: 'Description',
    Requirements: 'Requirements',
  };

  const navigate = useNavigate();

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
      switch (formType) {
        case FormType.Description:
          setDescPreview(true);
          break;
        case FormType.Requirements:
          setReqPreview(true);
          break;
        default:
          console.error('Failed on file handling');
      }
    }
  };

  const onCompareButton = () => {
    let body = new FormData();
    function appendFile(label) {
      body.append(label, files.get(label))
    }
    appendFile(FormType.Description)
    appendFile(FormType.Requirements)
    fetch('/upload', {
      method: 'POST',
      body: body
    }).then((response) => {
      navigate('/csv-table-view')
      response.json().then((body) => {
        console.log(response)
      })
        .catch(error => {
          console.error('failed to post file:', error);
        });
    });
    //
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
      default:
        console.error('Failed on type selection');
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
          {filename ? filename : 'No ' + (props.type === FormType.Description ? 'description' : 'requirements') + ' file selected yet'}
        </p>
      </label>
    </form>);
  }

  return (
    <div className='background'>
      <Particles
          id="tsparticles"
          init={particlesInit}
          options={particlesOptions}
      />
      <div className='app'>
        <div className="title-container">
          <h1 className="animated-title">Compare Documents</h1>
        </div>
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
          <div className="logo-container">
             <a href="https://www.gazprom-neft.ru/" target="gasprom-neft">
              <GaspromLogo className="company-logo" />
            </a>
            <a href="https://github.com/106-inc/womparator" target="gasprom-neft">
              <TeamLogo className="company-logo" />
            </a>
            <a href="https://mipt.ru/" target="mipt">
              <MiptLogo className="company-logo" />
            </a>
          </div>
          <div className="gasprom-container">
          </div>
        </main>
      </div>
    </div>
  );
}
