import React, { useState } from 'react';
import InputCodeEditor from '../components/InputCodeEditor';
import OutputCodeEditor from '../components/OutputCodeEditor';
import './Pages.css';
import '../styles/ButtonStyles.css'; // Import the existing button styles

const StartPage = () => {

    return (
        <div className='page-container'>
            <div className='editors-container'>
                <div className='left-box'>
                    <InputCodeEditor />
                </div>
                <div className='right-box'>
                    <OutputCodeEditor />
                </div>
            </div>
            <div className='center-button'>
                <button className="button-style" >
                    Migrate Code
                </button>
            </div>
        </div>
    );
};

export default StartPage;
