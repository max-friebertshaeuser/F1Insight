import { useEffect, useState } from 'react';
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

  if (loading) return <p className="text-center mt-20 text-gray-400">Evaluated bets loading...</p>;
  if (error) return <p className="text-center mt-20 text-red-500">{error}</p>;
  if (!data || data.bets.length === 0)
    return <p className="text-center mt-20 text-gray-400">No evaluated bets found.</p>;

  const groupedByRace = data.bets.reduce<Record<string, Bet[]>>((acc, bet) => {
    if (!acc[bet.race]) acc[bet.race] = [];
    acc[bet.race].push(bet);
    return acc;
  }, {});

  return (
    <div className="bg-[#0D0D11] text-white min-h-screen px-4 py-12 sm:px-6 lg:px-12">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-4xl font-extrabold text-center mb-16 tracking-tight">Evaluated Bets – Group: {groupName}</h2>

        <div className="space-y-16">
          {Object.entries(groupedByRace)
            .sort(([a], [b]) => new Date(b).getTime() - new Date(a).getTime())
            .map(([race, bets]) => (
              <div
                key={race}
                className="bg-gradient-to-br from-[#1c1c2b] to-[#14141e] rounded-2xl shadow-xl ring-1 ring-gray-800 p-6 sm:p-8 backdrop-blur-sm"
              >
                <h3 className="text-2xl font-semibold mb-6 text-white tracking-wide">🏁 Race: {race}</h3>

                <div className="overflow-x-auto scrollbar-thin scrollbar-thumb-gray-700">
                  <table className="min-w-full text-sm sm:text-base text-left">
                    <thead className="bg-[#2A2A3A] text-gray-300 sticky top-0 z-10">
                      <tr>
                        <th className="px-4 py-3">👤 User</th>
                        <th className="px-4 py-3">🥇 Top 3</th>
                        <th className="px-4 py-3">🔻 Last 5</th>
                        <th className="px-4 py-3">🔻 Last 10</th>
                        <th className="px-4 py-3">⚡ Fastest Round</th>
                        <th className="px-4 py-3 text-right">⭐ Points</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-700">
                      {bets.map((bet, i) => (
                        <tr key={`${race}-${bet.user}-${i}`} className="hover:bg-[#2a2a3a]/40 transition">
                          <td className="px-4 py-3 font-medium text-white">{bet.user}</td>
                          <td className="px-4 py-3 text-gray-100">{bet.bet_top_3.join(', ')}</td>
                          <td className="px-4 py-3 text-gray-300">{bet.bet_last_5}</td>
                          <td className="px-4 py-3 text-gray-300">{bet.bet_last_10}</td>
                          <td className="px-4 py-3 text-gray-300">{bet.bet_fastest_lap}</td>
                          <td className="px-4 py-3 text-right font-semibold text-yellow-400">{bet.points}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
