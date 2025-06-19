// src/pages/ShowBet.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

export default function ShowBet() {
  const { groupName, raceId } = useParams<{ groupName: string; raceId: string }>();
  const [bet, setBet] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE_BETTING}/${raceId}/show/`, {
          headers: getAuthHeaders(),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to fetch bet');
        setBet(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [raceId]);

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading bet...</p>;
  if (error) return <p className="text-center mt-20 text-red-400">{error}</p>;

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen p-6">
      <h2 className="text-3xl font-bold mb-6">Your Bet: {raceId}</h2>
      <div className="bg-gray-800 rounded-lg p-6 max-w-lg mx-auto space-y-4">
        <p><strong>Top 3:</strong> {bet.bet_top_3.join(', ')}</p>
        <p><strong>Last 5:</strong> {bet.bet_last_5}</p>
        <p><strong>Last 10:</strong> {bet.bet_last_10}</p>
        <p><strong>Fastest Lap:</strong> {bet.bet_fastest_lap}</p>
      </div>
      <div className="mt-6 flex justify-center space-x-4">
        <button onClick={() => navigate('edit')} className="px-4 py-2 bg-yellow-600 rounded hover:bg-yellow-700">
          Edit
        </button>
        <button onClick={() => navigate('delete')} className="px-4 py-2 bg-red-600 rounded hover:bg-red-700">
          Delete
        </button>
        <button onClick={() => navigate(-1)} className="px-4 py-2 bg-gray-600 rounded hover:bg-gray-500">
          Back
        </button>
      </div>
    </div>
  );
}
