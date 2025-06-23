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
            throw new Error(errData.username?.[0] || 'Failed to sign up');
        }

        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('username', data.username);

        navigate('/bettinggame');
        } catch (err: any) {
        setError(err.message);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-f1-black text-f1-white font-fregular px-4">
            <form
                onSubmit={(event => handleSubmit(event))}
                className="bg-[#1a1a1a] p-10 rounded-xl shadow-xl w-full max-w-xl min-w-[22rem] border border-f1-white/10"
            >

            <h1 className="text-5xl font-fwide mb-8 text-center text-white drop-shadow-xl break-words w-full">
                    Sign Up
                </h1>


                <div className="mb-6">
                    <label
                        htmlFor="username"
                        className="block text-sm mb-2 uppercase tracking-widest text-white/60 font-fregular"
                    >
                        Username
                    </label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        className="w-full bg-transparent border border-white/20 rounded px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-f1-white"
                        placeholder="Choose a username"
                    />
                </div>

                <div className="mb-6">
                    <label
                        htmlFor="mail"
                        className="block text-sm mb-2 uppercase tracking-widest text-white/60 font-fregular"
                    >
                        Email
                    </label>
                    <input
                        type="email"
                        id="mail"
                        value={mail}
                        onChange={(e) => setMail(e.target.value)}
                        required
                        className="w-full bg-transparent border border-white/20 rounded px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-f1-white"
                        placeholder="Your email address"
                    />
                </div>

                <div className="mb-6">
                    <label
                        htmlFor="password"
                        className="block text-sm mb-2 uppercase tracking-widest text-white/60 font-fregular"
                    >
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full bg-transparent border border-white/20 rounded px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-f1-white"
                        placeholder="Create a password"
                    />
                </div>

                {error && (
                    <p className="text-red-500 text-sm mb-6 text-center">{error}</p>
                )}

                <button
                    type="submit" onSubmit={handleSubmit}
                    className="w-full bg-f1-white text-f1-black font-fbold py-3 rounded hover:bg-white/90 transition-all"
                >
                    Join the Team
                </button>

                <p className="mt-6 text-sm text-center text-white/50">
                    Already have an account?{' '}
                    <Link to="/login" className="text-f1-white hover:underline">
                        Enter Grid
                    </Link>
                </p>
            </form>
        </div>
    );
}

export default Standings;