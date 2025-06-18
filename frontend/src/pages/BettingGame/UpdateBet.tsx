// src/pages/UpdateBet.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

function UpdateBet() {
  const { race_id } = useParams();
  const [betData, setBetData] = useState(null);
  const [betTop3, setBetTop3] = useState(['', '', '']);
  const [betLast5, setBetLast5] = useState('');
  const [betLast10, setBetLast10] = useState('');
  const [betFastestLap, setBetFastestLap] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API_BASE_BETTING}/${race_id}/show/`, { headers: getAuthHeaders() })
      .then(r => r.ok ? r.json() : Promise.reject('Failed to load'))
      .then(data => {
        setBetData(data);
        setBetTop3(data.bet_top_3);
        setBetLast5(data.bet_last_5);
        setBetLast10(data.bet_last_10);
        setBetFastestLap(data.bet_fastest_lap);
      })
      .catch(e => setError(e));
  }, [race_id]);

  const handleUpdate = async () => {
    try {
      const res = await fetch(`${API_BASE_BETTING}/${race_id}/update/`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ bet_top_3: betTop3, bet_last_5: betLast5, bet_last_10: betLast10, bet_fastest_lap: betFastestLap }),
      });
      if (!res.ok) throw new Error('Update failed');
      navigate(`/bets/${race_id}/show`);
    } catch (e) {
      setError(e.message);
    }
  };

  if (error) return <p className="text-red-500">{error}</p>;
  if (!betData) return <p>Loading...</p>;

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-4">Update Bet</h2>
      {betTop3.map((val, idx) => (
        <input
          key={idx}
          type="text"
          placeholder={`Top ${idx+1}`}
          value={val}
          onChange={e => { const arr = [...betTop3]; arr[idx]=e.target.value; setBetTop3(arr); }}
          className="block p-2 mb-2 bg-gray-700 rounded"
        />
      ))}
      <input
        type="text"
        placeholder="Last 5"
        value={betLast5}
        onChange={e => setBetLast5(e.target.value)}
        className="block p-2 mb-4 bg-gray-700 rounded"
      />
      <input
        type="text"
        placeholder="Last 10"
        value={betLast10}
        onChange={e => setBetLast10(e.target.value)}
        className="block p-2 mb-4 bg-gray-700 rounded"
      />
      <input
        type="text"
        placeholder="Fastest Lap"
        value={betFastestLap}
        onChange={e => setBetFastestLap(e.target.value)}
        className="block p-2 mb-4 bg-gray-700 rounded"
      />
      <button onClick={handleUpdate} className="p-2 bg-yellow-600 rounded">Save</button>
    </div>
  );
}
export default UpdateBet;