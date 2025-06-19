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

export default function SetBet() {
  const { groupName, raceId } = useParams<{ groupName: string; raceId: string }>();
  const navigate = useNavigate();

  const [options, setOptions] = useState<InfoResponse | null>(null);
  const [selTop3, setSelTop3] = useState<string[]>([]);
  const [selLast5, setSelLast5] = useState<string>('');
  const [selLast10, setSelLast10] = useState<string>('');
  const [selFastest, setSelFastest] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE_BETTING}/info/?race=${raceId}`, {
          headers: getAuthHeaders(),
        });
        const data: InfoResponse = await res.json();
        setOptions(data);
      } catch (e) {
        setError('Failed to load driver options');
      }
    })();
  }, [raceId]);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE_BETTING}/createbet`, {
        method: 'POST',
        headers: getAuthHeaders(),
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
      if (!res.ok) throw new Error(json.error || json.message || 'Submission failed');
      navigate(`/groups/${groupName}/bets`);
    } catch (e: any) {
      setError(e.message);
      setSubmitting(false);
    }
  };

  if (!options) return <p className="text-center mt-20 text-gray-400">Loading drivers...</p>;

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <h2 className="text-3xl font-bold text-center">Place Your Bet: {raceId} in group: {groupName}</h2>
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
            onClick={handleSubmit}
            className="flex-1 py-3 bg-green-600 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
          >
            {submitting ? 'Submitting...' : 'Submit Bet'}
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
