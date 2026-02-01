import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from '@/pages/LoginPage';
import { MainApp } from '@/pages/MainApp';
import '@/styles/theme.css';

export const App: React.FC = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsAuthenticated(!!token);
        setLoading(false);
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center" style={{ height: '100vh' }}>
                <div className="text-secondary">Loading...</div>
            </div>
        );
    }

    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/login"
                    element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />}
                />
                <Route
                    path="/*"
                    element={isAuthenticated ? <MainApp /> : <Navigate to="/login" />}
                />
            </Routes>
        </BrowserRouter>
    );
};
