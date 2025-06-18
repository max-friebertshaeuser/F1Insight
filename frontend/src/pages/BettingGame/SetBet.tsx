// src/pages/SetBet.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

function SetBet() {
  const [races, setRaces] = useState([]);
  const [raceId, setRaceId] = useState('');
  const [groupId, setGroupId] = useState('');
  const [betTop3, setBetTop3] = useState(['', '', '']);
  const [betLast5, setBetLast5] = useState('');
  const [betLast10, setBetLast10] = useState('');
  const [betFastestLap, setBetFastestLap] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API_BASE_BETTING}/available-races/`, { headers: getAuthHeaders() })
      .then(r => r.json())
      .then(data => setRaces([data]))
      .catch(e => setError(e.message));
  }, []);

  const handleSubmit = async () => {
    try {
      const res = await fetch(`${API_BASE_BETTING}/createbet`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ race: raceId, group: parseInt(groupId), bet_top_3: betTop3, bet_last_5: betLast5, bet_last_10: betLast10, bet_fastest_lap: betFastestLap }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || json.message || 'Error placing bet');
      navigate('/groups');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-4">Place a Bet</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <select value={raceId} onChange={e => setRaceId(e.target.value)} className="p-2 bg-gray-700 rounded mb-4">
        <option value="">Select Race</option>
        {races.map(r => <option key={r.id} value={r.id}>{r.circuit} - {r.date}</option>)}
      </select>
      <input type="number" placeholder="Group ID" value={groupId} onChange={e => setGroupId(e.target.value)} className="block p-2 mb-4 bg-gray-700 rounded" />
      {betTop3.map((val, idx) => <input key={idx} type="text" placeholder={`Top ${idx+1}`} value={val} onChange={e => { const arr = [...betTop3]; arr[idx]=e.target.value; setBetTop3(arr);} } className="block p-2 mb-2 bg-gray-700 rounded" />)}
      <input type="text" placeholder="Last 5" value={betLast5} onChange={e => setBetLast5(e.target.value)} className="block p-2 mb-4 bg-gray-700 rounded" />
      <input type="text" placeholder="Last 10" value={betLast10} onChange={e => setBetLast10(e.target.value)} className="block p-2 mb-4 bg-gray-700 rounded" />
      <input type="text" placeholder="Fastest Lap" value={betFastestLap} onChange={e => setBetFastestLap(e.target.value)} className="block p-2 mb-4 bg-gray-700 rounded" />
      <button onClick={handleSubmit} className="p-2 bg-green-600 rounded">Bet</button>
    </div>
  );
}
export default SetBet;