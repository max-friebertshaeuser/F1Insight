// src/pages/ShowBet.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

function ShowBet() {
  const { race_id } = useParams();
  const [bet, setBet] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API_BASE_BETTING}/${race_id}/show/`, { headers: getAuthHeaders() })
      .then(r => r.ok ? r.json() : Promise.reject('Failed to load'))
      .then(data => setBet(data))
      .catch(e => setError(e));
  }, [race_id]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!bet) return <p>Loading...</p>;

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-4">Your Bet for {bet.race}</h2>
      <p><strong>Top 3:</strong> {bet.bet_top_3.join(', ')}</p>
      <p><strong>Last 5:</strong> {bet.bet_last_5}</p>
      <p><strong>Last 10:</strong> {bet.bet_last_10}</p>
      <p><strong>Fastest Lap:</strong> {bet.bet_fastest_lap}</p>
      <div className="mt-4 space-x-2">
        <button onClick={() => navigate(`/bets/${race_id}/update`)} className="p-2 bg-yellow-600 rounded">Update</button>
        <button onClick={() => navigate(`/bets/${race_id}/delete`)} className="p-2 bg-red-600 rounded">Delete</button>
      </div>
    </div>
  );
}
export default ShowBet;