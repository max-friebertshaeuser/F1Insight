import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

interface BetStat {
  user: string;
  points: number;
}

interface GroupInfoData {
  group_name: string;
  owner: string;
  bet_stats: BetStat[];
}

const JoinGroup: React.FC = () => {
  const { groupName } = useParams<{ groupName: string }>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!groupName) return;
    (async () => {
      try {
        const res = await fetch(`${API_BASE_GROUPS}/getgroupinfo/`, {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({ group_name: groupName }),
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.status || err.error || 'Fehler beim Laden');
        }
        const data: GroupInfoData = await res.json();

        const currentUser = localStorage.getItem('username');
        const member = data.bet_stats.some(bs => bs.user === currentUser);

        if (member) {
          navigate(`/groups/${groupName}`, { replace: true });
          return;
        }
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [groupName, navigate]);

  const handleJoin = async () => {
    try {
      const res = await fetch(`${API_BASE_GROUPS}/join/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ group_name: groupName }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.status || json.error || 'error while joining group');
      navigate(`/groups/${groupName}`, { replace: true });
    } catch (err: any) {
      setError(err.message);
    }
  };

  // 3) UI
  if (loading) {
    return <p className="text-center mt-20 text-gray-400">Loading...</p>;
  }
  if (error) {
    return <p className="text-center mt-20 text-red-500">{error}</p>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white p-6">
      <h1 className="text-3xl font-bold mb-4">Join group</h1>
      <p className="mb-6 text-lg">
        Do you want to join the group <span className="font-semibold">{groupName}</span>?
      </p>
      <button
        onClick={handleJoin}
        className="px-6 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition"
      >
        Join
      </button>
    </div>
  );
};

export default JoinGroup;
