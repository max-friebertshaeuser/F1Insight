// src/pages/JoinGroup.tsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

interface Group {
  group_id: number;
  group_name: string;
  join_link: string; // join_id comes back as join_link
}

const JoinGroup: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);
  const [selectedGroupId, setSelectedGroupId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const res = await fetch(`${API_BASE_GROUPS}/getallgroups/`, {
          headers: getAuthHeaders(),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.status || 'Fehler beim Laden der Gruppen');
        setGroups(json.groups);
      } catch (err: any) {
        setError(err.message);
      }
    };
    fetchGroups();
  }, []);

  const handleJoin = async () => {
    if (selectedGroupId === null) return;
    const group = groups.find(g => g.group_id === selectedGroupId);
    if (!group) return;
    try {
      const res = await fetch(`${API_BASE_GROUPS}/join/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          group_name: group.group_name,
          join_id: group.join_link,
        }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.status || json.error || 'Fehler beim Beitreten');
      navigate('/groups');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white">
      <h1 className="text-4xl font-bold mb-6">Gruppe beitreten</h1>

      {error && <p className="mb-4 text-red-500">{error}</p>}

      <select
        value={selectedGroupId ?? ''}
        onChange={e => setSelectedGroupId(e.target.value ? parseInt(e.target.value) : null)}
        className="w-full max-w-sm p-2 mb-4 bg-gray-700 rounded"
      >
        <option value="">Wähle eine Gruppe</option>
        {groups.map(g => (
          <option key={g.group_id} value={g.group_id}>
            {g.group_name}
          </option>
        ))}
      </select>

      <button
        onClick={handleJoin}
        disabled={selectedGroupId === null}
        className="w-full max-w-sm p-2 bg-blue-600 rounded disabled:opacity-50"
      >
        Beitreten
      </button>
    </div>
  );
};

export default JoinGroup;
