import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');

  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();

useEffect(() => {
    if (isAuthenticated) {
      navigate('/bettinggame', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'error while logging in');
      }

      const data = await response.json();

      login(username, data.access, data.refresh);

      navigate('/bettinggame', { replace: true });
    } catch (err: any) {
      setError(err.message || 'unknown error occurred');
    }
  };

  return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-f1-black text-f1-white font-fregular px-4">
        <form
            onSubmit={handleSubmit}
            className="bg-[#1a1a1a] p-10 rounded-xl shadow-xl w-full max-w-md border border-f1-white/10"
        >
          <h1 className="text-5xl font-fwide mb-8 text-center text-white drop-shadow-xl">
            Log In
          </h1>

          <div className="mb-6">
            <label htmlFor="username" className="block text-sm mb-2 uppercase tracking-widest text-white/60 font-fregular">
              Username
            </label>
            <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full bg-transparent border border-white/20 rounded px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-f1-white"
                placeholder="Your username"
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-sm mb-2 uppercase tracking-widest text-white/60 font-fregular">
              Password
            </label>
            <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-transparent border border-white/20 rounded px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-f1-white"
                placeholder="Your password"
            />
          </div>

          {error && (
              <p className="text-red-500 text-sm mb-6 text-center">{error}</p>
          )}

          <button
              type="submit"
              className="w-full bg-f1-white text-f1-black font-fbold py-3 rounded hover:bg-white/90 transition-all"
          >
            Enter Grid
          </button>

          <p className="mt-6 text-sm text-center text-white/50">
            No account?{' '}
            <Link to="/register" className="text-f1-white hover:underline">
              Join the team
            </Link>
          </p>
        </form>
      </div>
  );
};

export default Login;
