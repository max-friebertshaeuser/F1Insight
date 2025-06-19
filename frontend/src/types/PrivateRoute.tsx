import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthFetch } from '../utils/authFetch';

const PrivateRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const authFetch = useAuthFetch();
  const [loading, setLoading] = useState(true);
  const [authOk, setAuthOk] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await authFetch('http://localhost:8000/api/auth/profile/');
        setAuthOk(response.ok);
      } catch {
        setAuthOk(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [authFetch]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-gray-400 text-lg">
        Loading...
      </div>
    );
  }

  return authOk ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
