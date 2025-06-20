import { useAuth } from '../contexts/AuthContext';

export const useAuthFetch = () => {
  const { refreshAccessToken, logout } = useAuth();

  const authFetch = async (url: string, options: RequestInit = {}) => {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    if (!accessToken && !refreshToken) {
      logout();
      return new Response(null, { status: 401, statusText: 'Unauthorized' });
    }

    if (!accessToken) {
      console.log('[authFetch] no access_token found');
      logout();
      return new Response(null, { status: 401, statusText: 'Unauthorized' });
    }

    if (!refreshToken) {
      console.log('[authFetch] no refresh_token found');
    }

    console.log(`[authFetch] request to ${url} started with access_token`);

    const headers = {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
    };

    let response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
      console.log('[authFetch] 401 received – try refreshAccessToken()');

      const refreshed = await refreshAccessToken();

      if (refreshToken && refreshed) {
        console.log('[authFetch] Token refresh successful – retry request');
        const newAccessToken = localStorage.getItem('access_token');
        const retryHeaders = {
          ...options.headers,
          Authorization: `Bearer ${newAccessToken}`,
        };
        response = await fetch(url, { ...options, headers: retryHeaders });
        console.log(`[authFetch] renewed request finished with ${response.status}`);
      } else {
        console.log('[authFetch] token could not be refreshed – logout');
        logout();
        return new Response(null, { status: 401, statusText: 'Unauthorized' });
      }
    } else {
      console.log(`[authFetch] request to ${url} finished with ${response.status}`);
    }

    return response;
  };

  return authFetch;
};
