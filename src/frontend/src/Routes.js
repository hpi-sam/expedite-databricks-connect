// src/Routes.js
import React from 'react';
import { Routes, Route } from 'react-router-dom'; 
import UploadPage from './pages/UploadPage'; 

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<UploadPage />} />
        </Routes>
    );
};
