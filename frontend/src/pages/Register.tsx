import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
function Standings() {
    const [username, setUsername] = useState<string>('');
    const [mail, setMail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string>('');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
        const response = await fetch('http://localhost:8000/api/auth/register/', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Failed to sign up');
        }

        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        // Weiterleitung zur Profil-Seite
        navigate('/bettinggame');
        } catch (err: any) {
        setError(err.message);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white">
            <form
            onSubmit={handleSubmit}
            className="bg-black p-6 rounded-lg shadow-md w-full max-w-sm"
        >
            <h1 className="text-4xl font-bold mb-6">Register</h1>

            <div className="mb-4">
            <label htmlFor="username" className="block text-sm font-medium mb-1">
                username
            </label>
            <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full border border-gray-300 rounded px-3 py-2"
            />
            </div>

            <div className="mb-4">
            <label htmlFor="mail" className="block text-sm font-medium mb-1">
                mail
            </label>
            <input
                type="text"
                id="mail"
                value={mail}
                onChange={(e) => setMail(e.target.value)}
                required
                className="w-full border border-gray-300 rounded px-3 py-2"
            />
            </div>

            <div className="mb-4">
            <label htmlFor="password" className="block text-sm font-medium mb-1">
                password
            </label>
            <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full border border-gray-300 rounded px-3 py-2"
            />
            </div>

            {error && (
            <p className="text-red-600 text-sm mb-4 text-center">{error}</p>
            )}

            <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
            >
            Sign up
            </button>
            <p className="mt-4 text-sm text-center">
                Already have an account?{' '}
                <Link to="/login" className="text-blue-400 hover:underline">
                    Log in
                </Link>
            </p>        
        </form>
        </div>
    );
}

export default Standings;