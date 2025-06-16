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
        if (response.ok) {
          setAuthOk(true);
        } else {
          setAuthOk(false);
        }
      } catch {
        setAuthOk(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [authFetch]);

  if (loading) return <div>Lade...</div>;

  return authOk ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
