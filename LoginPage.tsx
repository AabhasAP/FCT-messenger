import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '@/services/api';
import '@/styles/theme.css';
import './LoginPage.css';

export const LoginPage: React.FC = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            let response;
            if (isLogin) {
                response = await authAPI.login(email, password);
            } else {
                response = await authAPI.register({ email, password, full_name: fullName });
            }

            const { access_token, refresh_token } = response.data;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);

            navigate('/');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Authentication failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card glass">
                <div className="login-header">
                    <h1>Forensic Cyber Tech</h1>
                    <p className="text-secondary">Cloud Messenger</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    {!isLogin && (
                        <div className="form-group">
                            <label>Full Name</label>
                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                placeholder="Enter your full name"
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" className="btn btn-primary w-full" disabled={loading}>
                        {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Sign Up'}
                    </button>
                </form>

                <div className="login-footer">
                    <button
                        type="button"
                        className="link-button"
                        onClick={() => {
                            setIsLogin(!isLogin);
                            setError('');
                        }}
                    >
                        {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
                    </button>
                </div>
            </div>

            <div className="cyber-grid"></div>
        </div>
    );
};
