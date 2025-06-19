// src/pages/GroupsList.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

interface Group {
  group_id: number;
  group_name: string;
  members: string[];
}

const GroupsList: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const currentUser = localStorage.getItem('username') || '';

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const res = await fetch(`${API_BASE_GROUPS}/getallgroups/`, {
          headers: getAuthHeaders(),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.status || 'Failed to load groups');
        setGroups(json.groups);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchGroups();
  }, []);

  if (loading) {
    return <p className="text-center mt-20 text-gray-400">Loading groups...</p>;
  }
  if (error) {
    return <p className="text-center mt-20 text-red-500">{error}</p>;
  }

  const myGroups = groups.filter(g => g.members.includes(currentUser));

  if (myGroups.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white p-6">
        <p className="text-lg mb-4">You’re not a member of any group yet.</p>
        <Link
          to="/groups/create"
          className="inline-block px-6 py-2 bg-blue-600 rounded-full hover:bg-blue-700 transition"
        >
          Create a new group
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-extrabold mb-16 text-center">My Groups</h2>
        <div className="grid justify-center grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {myGroups.map(g => (
            <Link
              key={g.group_id}
              to={`/groups/${g.group_name}`}
              className="group relative flex flex-col p-6 bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition duration-300 max-w-xs"
            >
              {/* Ribbon with member count */}
              <div className="absolute top-4 right-4 bg-blue-600 text-xs uppercase px-2 py-1 rounded-full">
                {g.members.length} Member{g.members.length > 1 ? 's' : ''}
              </div>

              {/* Icon */}
              <div className="mb-4 flex justify-center">
                <div className="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center text-2xl text-blue-400 font-bold">
                  {g.group_name.charAt(0).toUpperCase()}
                </div>
              </div>

              {/* Name */}
              <h3 className="text-2xl font-bold mb-2 text-center">{g.group_name}</h3>

              {/* Avatars */}
              <div className="flex justify-center space-x-2 mb-4">
                {g.members.slice(0, 4).map((u, idx) => (
                  <div
                    key={idx}
                    className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center text-sm"
                    title={u}
                  >
                    {u.charAt(0).toUpperCase()}
                  </div>
                ))}
                {g.members.length > 4 && (
                  <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center text-sm">
                    +{g.members.length - 4}
                  </div>
                )}
              </div>

              {/* CTA */}
              <span className="mt-auto inline-block text-center px-4 py-2 bg-blue-600 rounded-lg text-sm font-medium hover:bg-blue-700 transition">
                View Group
              </span>
            </Link>
          ))}

          {/* Create New Group Card */}
          <Link
            to="/groups/create"
            className="flex flex-col items-center justify-center p-6 bg-gray-800 bg-opacity-50 rounded-2xl border-2 border-dashed border-gray-600 hover:bg-opacity-75 transform hover:scale-105 transition duration-300 max-w-xs"
          >
            <div className="text-5xl font-bold text-gray-500 mb-2">+</div>
            <h3 className="text-xl font-semibold text-gray-300">New Group</h3>
            <p className="mt-2 text-sm text-gray-400 text-center">Create your own group</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default GroupsList;
