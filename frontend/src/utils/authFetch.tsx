// src/utils/authFetch.ts
import { useAuth } from '../contexts/AuthContext';

export const useAuthFetch = () => {
  const { refreshAccessToken, logout } = useAuth();

  const authFetch = async (url: string, options: RequestInit = {}) => {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    // 🔒 Wenn beide Tokens fehlen → stillschweigend Logout & Redirect
    if (!accessToken && !refreshToken) {
      logout();
      return new Response(null, { status: 401, statusText: 'Unauthorized' });
    }

    // 📢 Wenn nur einer fehlt → Logging & Logout
    if (!accessToken) {
      console.log('[authFetch] Kein access_token vorhanden');
      logout();
      return new Response(null, { status: 401, statusText: 'Unauthorized' });
    }

    if (!refreshToken) {
      console.log('[authFetch] Kein refresh_token vorhanden');
    }

    // ✅ Zugriff mit vorhandenem access_token
    console.log(`[authFetch] Anfrage an ${url} gestartet mit access_token`);

    const headers = {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
    };

    let response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
      console.log('[authFetch] 401 erhalten – versuche refreshAccessToken()');

      const refreshed = await refreshAccessToken();

      if (refreshToken && refreshed) {
        console.log('[authFetch] Token erfolgreich erneuert – wiederhole Anfrage');
        const newAccessToken = localStorage.getItem('access_token');
        const retryHeaders = {
          ...options.headers,
          Authorization: `Bearer ${newAccessToken}`,
        };
        response = await fetch(url, { ...options, headers: retryHeaders });
        console.log(`[authFetch] Erneute Anfrage abgeschlossen mit Status ${response.status}`);
      } else {
        console.log('[authFetch] Token konnte nicht erneuert werden – logout');
        logout();
        return new Response(null, { status: 401, statusText: 'Unauthorized' });
      }
    } else {
      console.log(`[authFetch] Anfrage an ${url} abgeschlossen mit Status ${response.status}`);
    }

    return response;
  };

  return authFetch;
};
