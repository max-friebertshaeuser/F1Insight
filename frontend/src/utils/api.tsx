export const API_BASE_GROUPS = 'http://localhost:8000/api/betting/groups';
export const API_BASE_BETTING = 'http://localhost:8000/api/betting/bets';

export function getAuthHeaders() {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    Authorization: token ? `Bearer ${token}` : '',
  };
}
