// src/pages/GroupInfo.tsx
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

interface BetStat { user: string; points: number; }
interface GroupInfoData { group_name: string; owner: string; bet_stats: BetStat[]; }

export default function GroupInfo() {
  const { groupName } = useParams<{ groupName: string }>();
  const [info, setInfo] = useState<GroupInfoData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!groupName) return;
    (async () => {
      try {
        const res = await fetch(`${API_BASE_GROUPS}/getgroupinfo/`, {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({ group_name: groupName }),
        });
        if (!res.ok) throw await res.json();
        const data: GroupInfoData = await res.json();
        setInfo(data);
      } catch (e: any) {
        setError(e.status || e.error || 'Fehler beim Laden');
      } finally {
        setLoading(false);
      }
    })();
  }, [groupName]);

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading…</p>;
  if (error)   return <p className="text-center mt-20 text-red-500">{error}</p>;
  if (!info)  return null;

  // Sort top 3
  const sorted = [...info.bet_stats].sort((a, b) => b.points - a.points);
  const [first, second, third, ...rest] = sorted;

  return (
    <div className="flex flex-col items-center bg-[#0F0F17] text-white min-h-screen py-10 px-4">
      {/* Header */}
      <div className="w-full max-w-2xl text-center mb-12">
        <h1 className="text-4xl font-bold">{info.group_name}</h1>
        <p className="mt-2 text-lg">
          Owner: <span className="font-semibold">{info.owner}</span>
        </p>
        <p className="mt-1 text-sm text-gray-400">
          Join-Link:&nbsp;
          <Link
            to={`${window.location.pathname}/join`}
            className="text-blue-400 hover:underline"
          >
            {window.location.origin + window.location.pathname + '/join'}
          </Link>
        </p>
      </div>

      {/* Podium */}
      <div className="flex items-end space-x-8 mb-12">
        {second && (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-gray-600 rounded-full flex items-center justify-center text-xl font-bold">
              2
            </div>
            <p className="mt-2">{second.user}</p>
            <p className="text-sm text-gray-400">{second.points} Pkt.</p>
          </div>
        )}
        {first && (
          <div className="flex flex-col items-center">
            <div className="w-20 h-20 bg-yellow-400 rounded-full flex items-center justify-center text-2xl font-bold">
              1
            </div>
            <p className="mt-2">{first.user}</p>
            <p className="text-sm text-gray-400">{first.points} Pkt.</p>
          </div>
        )}
        {third && (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-yellow-700 rounded-full flex items-center justify-center text-xl font-bold">
              3
            </div>
            <p className="mt-2">{third.user}</p>
            <p className="text-sm text-gray-400">{third.points} Pkt.</p>
          </div>
        )}
      </div>

      {/* Remaining */}
      {rest.length > 0 && (
        <div className="w-full max-w-2xl bg-gray-800 rounded-lg shadow p-6 mb-12">
          <h2 className="text-2xl font-semibold mb-4">Additional Rankings</h2>
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="py-2">Rank</th>
                <th className="py-2">User</th>
                <th className="py-2">Points</th>
              </tr>
            </thead>
            <tbody>
              {rest.map((bs, idx) => (
                <tr key={bs.user} className="hover:bg-gray-700">
                  <td className="py-2">{idx + 4}</td>
                  <td className="py-2">{bs.user}</td>
                  <td className="py-2">{bs.points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Actions */}
      <div className="flex space-x-4">
        <Link
          to={`/groups/${groupName}/evaluated`}
          className="px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition"
        >
          Evaluated Bets
        </Link>
        <Link
          to={`/groups/${groupName}/bets`}
          className="px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition"
        >
          Manage Bets
        </Link>
        <Link
          to={`/groups/${groupName}/leave`}
          className="px-6 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition"
        >
          Leave group
        </Link>
        <Link
          to="/bettinggame"
          className="px-6 py-2 bg-gray-600 rounded-lg hover:bg-gray-500 transition"
        >
          Back to Betting Game Start
        </Link>
      </div>
    </div>
  );
}
