// src/pages/UpdateBet.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';
import type { Driver } from '../../types/driver';
import ScrollableDriverSelector from '../../components/ScrollableDriverSelector';

interface InfoResponse {
  drivers: Driver[];
  last5: Driver[];
  mid5: Driver[];
}

interface BetDetail {
  bet_top_3: string[];
  bet_last_5: string;
  bet_last_10: string;
  bet_fastest_lap: string;
}

export default function UpdateBet() {
  const { groupName, raceId } = useParams<{ groupName: string; raceId: string }>();
  const navigate = useNavigate();

  const [options, setOptions] = useState<InfoResponse | null>(null);
  const [existingBet, setExistingBet] = useState<BetDetail | null>(null);

  const [selTop3, setSelTop3] = useState<string[]>([]);
  const [selLast5, setSelLast5] = useState<string>('');
  const [selLast10, setSelLast10] = useState<string>('');
  const [selFastest, setSelFastest] = useState<string>('');

  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        // Load driver options
        const infoRes = await fetch(`${API_BASE_BETTING}/info/?race=${raceId}`, {
          headers: getAuthHeaders(),
        });
        const infoData: InfoResponse = await infoRes.json();
        setOptions(infoData);

        // Load existing bet
        const betRes = await fetch(`${API_BASE_BETTING}/${raceId}/show/`, {
          method: 'POST',
          headers: {
            ...getAuthHeaders(),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ group: groupName, race: raceId }),
        });

        const betData: BetDetail = await betRes.json();
        if (!betRes.ok) throw new Error(betData ? betData.toString() : 'Failed to fetch bet');

        setExistingBet(betData);
        setSelTop3(betData.bet_top_3 || []);
        setSelLast5(betData.bet_last_5 || '');
        setSelLast10(betData.bet_last_10 || '');
        setSelFastest(betData.bet_fastest_lap || '');
      } catch (e: any) {
        setError(e.message || 'Failed to load bet or drivers');
      } finally {
        setLoading(false);
      }
    })();
  }, [groupName, raceId]);

  const handleUpdate = async () => {
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE_BETTING}/${raceId}/update/`, {
        method: 'PUT',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          group: groupName,
          race: raceId,
          bet_top_3: selTop3,
          bet_last_5: selLast5,
          bet_last_10: selLast10,
          bet_fastest_lap: selFastest,
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

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading bet & driver data...</p>;
  if (error) return <p className="text-center mt-20 text-red-400">{error}</p>;
  if (!options) return null;

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <h2 className="text-3xl font-bold text-center">Edit Your Bet: {raceId}</h2>
        {error && <p className="text-red-500 text-center">{error}</p>}

        <ScrollableDriverSelector
          title="Top 3"
          drivers={options.drivers}
          name="top3"
          selection={selTop3}
          onSelect={(id) => {
            if (!selTop3.includes(id) && selTop3.length < 3) {
              setSelTop3([...selTop3, id]);
            } else if (selTop3.includes(id)) {
              setSelTop3(selTop3.filter(d => d !== id));
            }
          }}
          type="checkbox"
          limit={3}
        />

        <ScrollableDriverSelector
          title="Last 5"
          drivers={options.last5}
          name="last5"
          selection={selLast5}
          onSelect={setSelLast5}
        />

        <ScrollableDriverSelector
          title="Last 10"
          drivers={options.drivers.slice(-10)}
          name="last10"
          selection={selLast10}
          onSelect={setSelLast10}
        />

        <ScrollableDriverSelector
          title="Fastest Lap"
          drivers={options.drivers}
          name="fastest"
          selection={selFastest}
          onSelect={setSelFastest}
        />

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            disabled={submitting}
            onClick={handleUpdate}
            className="flex-1 py-3 bg-yellow-600 rounded-lg hover:bg-yellow-700 transition disabled:opacity-50"
          >
            {submitting ? 'Updating...' : 'Update Bet'}
          </button>
          <button
            onClick={() => navigate(-1)}
            className="flex-1 py-3 bg-gray-600 rounded-lg hover:bg-gray-500 transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
