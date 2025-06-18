// src/pages/GroupsList.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

interface Group {
  group_id: number;
  group_name: string;
}

const GroupsList: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const res = await fetch(`${API_BASE_GROUPS}/getallgroups/`, {
          headers: getAuthHeaders(),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.status || 'Fehler beim Laden');
        setGroups(json.groups);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchGroups();
  }, []);

  if (loading) return <p>Lade Gruppen...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Meine Gruppen</h2>
      <ul className="space-y-2">
        {groups.map((g) => (
          <li key={g.group_id} className="p-4 border rounded-lg">
            <Link to={`/groups/${g.group_id}`} className="text-blue-400 hover:underline">
              {g.group_name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GroupsList;
