import React, { useState } from 'react';
import InputCodeEditor from '../components/InputCodeEditor';
import OutputCodeEditor from '../components/OutputCodeEditor';
import Button from '@mui/material/Button'; // Import MUI Button
import Stack from '@mui/material/Stack';

import './Pages.css';

const StartPage = () => {
  const handleButtonClick = () => {
    alert('Migrate Code button clicked!');
  };

  return (
    <div className="page-container">
      <div className="editors-container">
        <div className="left-box">
          <InputCodeEditor />
        </div>
        <div className="right-box">
          <OutputCodeEditor />
        </div>
      </div>
      <div className="center-button">
        <Stack spacing={2} direction="row">
          {/* MUI Button with click event */}
          <Button 
              variant="contained" 
              onClick={handleButtonClick}
              style={{ backgroundColor: '#b20036'}}
            >
              Migrate
          </Button>
        </Stack>
      </div>
    </div>
  );
};

export default StartPage;
