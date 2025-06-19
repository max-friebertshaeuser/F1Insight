import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getAuthHeaders } from '../../utils/api';

interface Bet {
  user: string;
  race: string;
  points: number;
  bet_top_3: string[];
  bet_last_5: string;
  bet_last_10: string;
  bet_fastest_lap: string;
}

interface StandingsEntry {
  user: string;
  points: number;
}

interface ResponseData {
  bets: Bet[];
  standings: StandingsEntry[];
}

export default function EvaluatedBetsTable() {
  const { groupName } = useParams<{ groupName: string }>();
  const [data, setData] = useState<ResponseData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('http://localhost:8000/api/betting/bets/evaluated-bets/', {
          method: 'POST',
          headers: {
            ...getAuthHeaders(),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ group: groupName }),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || 'Failed to load evaluated bets');
        setData(json);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [groupName]);

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading evaluated bets...</p>;
  if (error) return <p className="text-center mt-20 text-red-400">{error}</p>;
  if (!data || data.bets.length === 0) return <p className="text-center mt-20 text-gray-400">No evaluated bets found.</p>;

  // Gruppiere Bets nach Race
  const groupedByRace = data.bets.reduce<Record<string, Bet[]>>((acc, bet) => {
    if (!acc[bet.race]) acc[bet.race] = [];
    acc[bet.race].push(bet);
    return acc;
  }, {});

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-6 text-center">Ausgewertete Tipps für Gruppe: {groupName}</h2>

        {Object.entries(groupedByRace).sort(([a], [b]) => new Date(b).getTime() - new Date(a).getTime()).map(([race, bets]) => (
          <div key={race} className="mb-10 border border-gray-700 rounded-lg p-6 bg-[#1A1A2A]">
            <h3 className="text-xl font-semibold mb-4">🏁 Rennen: {race}</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm text-left">
                <thead className="bg-[#2A2A3A] text-gray-300">
                  <tr>
                    <th className="px-4 py-2">👤 Nutzer</th>
                    <th className="px-4 py-2">🥇 Top 3</th>
                    <th className="px-4 py-2">🔻 Last 5</th>
                    <th className="px-4 py-2">🔻 Last 10</th>
                    <th className="px-4 py-2">⚡ Fastest Lap</th>
                    <th className="px-4 py-2 text-right">⭐ Punkte</th>
                  </tr>
                </thead>
                <tbody>
                  {bets.map(bet => (
                    <tr key={`${race}-${bet.user}`} className="border-t border-gray-700">
                      <td className="px-4 py-2">{bet.user}</td>
                      <td className="px-4 py-2">{bet.bet_top_3.join(', ')}</td>
                      <td className="px-4 py-2">{bet.bet_last_5}</td>
                      <td className="px-4 py-2">{bet.bet_last_10}</td>
                      <td className="px-4 py-2">{bet.bet_fastest_lap}</td>
                      <td className="px-4 py-2 text-right font-semibold">{bet.points}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
