// src/pages/DeleteBet.tsx
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

export default function DeleteBet() {
  const { groupName, raceId } = useParams<{ groupName: string; raceId: string }>();
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);
  const navigate = useNavigate();

  const handleDelete = async () => {
    setDeleting(true);
    try {
      const res = await fetch(`${API_BASE_BETTING}/${raceId}/delete/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || json.message || 'Delete failed');
      navigate(`/groups/${groupName}/bets`);
    } catch (e: any) {
      setError(e.message);
      setDeleting(false);
    }
  };

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen p-6 flex flex-col items-center justify-center">
      <h2 className="text-3xl font-bold mb-6">Delete Bet: {raceId}?</h2>
      {error && <p className="text-red-400 mb-4">{error}</p>}
      <div className="flex space-x-4">
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="px-6 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
        >
          {deleting ? 'Deleting...' : 'Yes, Delete'}
        </button>
        <button
          onClick={() => navigate(-1)}
          className="px-6 py-2 bg-gray-600 rounded-lg hover:bg-gray-500 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
