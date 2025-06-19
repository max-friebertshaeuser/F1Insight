// src/pages/RaceBets.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

interface Race {
  id: string;
  season: string;
  circuit: string;
  date: string;
}

export default function RaceBets() {
  const { groupName } = useParams<{ groupName: string }>();
  const [races, setRaces] = useState<Race[]>([]);
  const [bets, setBets] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const rRes = await fetch(`${API_BASE_BETTING}/available-races/`, {
          headers: getAuthHeaders(),
          // group_name included in later endpoints
        });
        const race: Race = await rRes.json();
        setRaces([race]);

        // Check bet existence
        const bInfo: Record<string, boolean> = {};
        for (let rc of [race]) {
          const res = await fetch(
            `${API_BASE_BETTING}/${rc.id}/show/`,
            {
              headers: getAuthHeaders(),
              // Body: { group_name }
              body: JSON.stringify({ group_name: groupName })
            }
          );
          bInfo[rc.id] = res.ok;
        }
        setBets(bInfo);
      } finally {
        setLoading(false);
      }
    })();
  }, [groupName]);

  if (loading) return <p className="text-center mt-20">Loading...</p>;

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen py-10 px-4">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold mb-8 text-center">Betting in {groupName}</h2>

        <div className="space-y-6">
          {races.map(race => (
            <div key={race.id} className="flex flex-col sm:flex-row items-center justify-between bg-gray-800 rounded-xl p-6 shadow-lg">
              <div>
                <h3 className="text-xl font-semibold">{race.circuit}</h3>
                <p className="text-gray-400">{race.date} · Season {race.season}</p>
              </div>

              <div className="mt-4 sm:mt-0 space-x-2">
                {!bets[race.id] ? (
                  <button
                    onClick={() => navigate(`set/${race.id}`)}
                    className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-700 transition"
                  >
                    Place Bet
                  </button>
                ) : (
                  <>
                    <button
                      onClick={() => navigate(`view/${race.id}`)}
                      className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition"
                    >
                      View Bet
                    </button>
                    <button
                      onClick={() => navigate(`edit/${race.id}`)}
                      className="px-4 py-2 bg-yellow-600 rounded-lg hover:bg-yellow-700 transition"
                    >
                      Edit Bet
                    </button>
                    <button
                      onClick={() => navigate(`delete/${race.id}`)}
                      className="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition"
                    >
                      Delete Bet
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
