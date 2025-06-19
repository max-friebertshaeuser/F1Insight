// src/pages/UpdateBet.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

export default function UpdateBet() {
  const { groupName, raceId } = useParams<{ groupName: string; raceId: string }>();
  const navigate = useNavigate();
  const [form, setForm] = useState({ top3: ['', '', ''], last5: '', last10: '', fastest: '' });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE_BETTING}/${raceId}/show/`, {
          headers: getAuthHeaders(),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to load');
        setForm({
          top3: data.bet_top_3,
          last5: data.bet_last_5,
          last10: data.bet_last_10,
          fastest: data.bet_fastest_lap
        });
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [raceId]);

  const handleUpdate = async () => {
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE_BETTING}/${raceId}/update/`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          group_name: groupName,
          race: raceId,
          bet_top_3: form.top3,
          bet_last_5: form.last5,
          bet_last_10: form.last10,
          bet_fastest_lap: form.fastest,
        }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || json.message || 'Update failed');
      navigate(`/groups/${groupName}/bets`);
    } catch (e: any) {
      setError(e.message);
      setSubmitting(false);
    }
  };

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading bet data...</p>;
  if (error) return <p className="text-center mt-20 text-red-400">{error}</p>;

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen p-6 flex flex-col items-center">
      <h2 className="text-3xl font-bold mb-6">Edit Bet: {raceId}</h2>
      <div className="space-y-4 w-full max-w-lg">
        <div>
          <label>Top 3 (comma-separated)</label>
          <input
            value={form.top3.join(',')}
            onChange={e => setForm(s => ({ ...s, top3: e.target.value.split(',').map(t => t.trim()) }))}
            className="w-full p-2 bg-gray-800 rounded"
          />
        </div>
        <div>
          <label>Last 5</label>
          <input
            value={form.last5}
            onChange={e => setForm(s => ({ ...s, last5: e.target.value }))}
            className="w-full p-2 bg-gray-800 rounded"
          />
        </div>
        <div>
          <label>Last 10</label>
          <input
            value={form.last10}
            onChange={e => setForm(s => ({ ...s, last10: e.target.value }))}
            className="w-full p-2 bg-gray-800 rounded"
          />
        </div>
        <div>
          <label>Fastest Lap</label>
          <input
            value={form.fastest}
            onChange={e => setForm(s => ({ ...s, fastest: e.target.value }))}
            className="w-full p-2 bg-gray-800 rounded"
          />
        </div>

        <button
          onClick={handleUpdate}
          disabled={submitting}
          className="w-full py-3 bg-yellow-600 rounded-lg hover:bg-yellow-700 transition disabled:opacity-50"
        >
          {submitting ? 'Updating...' : 'Update Bet'}
        </button>

        <button
          onClick={() => navigate(-1)}
          className="w-full py-3 bg-gray-600 rounded-lg hover:bg-gray-500 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
