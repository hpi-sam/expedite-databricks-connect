// src/Routes.js
import React from 'react';
import { Routes, Route } from 'react-router-dom'; 
import StartPage from './pages/StartPage'; 

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<StartPage />} />
        </Routes>
    );
};
