import { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';

const Logout = () => {
  const { logout } = useAuth();

  useEffect(() => {
    logout();
  }, [logout]);

  // Nach dem Logout zur Login-Seite weiterleiten
  return <Navigate to="/login" replace />;
};

export default Logout;
