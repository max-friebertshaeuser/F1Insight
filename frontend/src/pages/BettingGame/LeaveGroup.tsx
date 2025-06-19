// src/pages/LeaveGroup.tsx
import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

const LeaveGroup: React.FC = () => {
  const { groupName } = useParams<{ groupName: string }>();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLeave = async () => {
    if (!groupName) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_GROUPS}/leave/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ group_name: groupName }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.status || json.error || 'Fehler beim Verlassen');
      navigate('/bettinggame');
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (groupName) {
      navigate(`/groups/${groupName}`);
    } else {
      navigate('/bettinggame');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white p-6">
      <h1 className="text-4xl font-bold mb-4">Leave group</h1>
      <p className="mb-6 text-lg">
        Are you sure to leave the group <span className="font-semibold">{groupName}</span>?
      </p>
      {error && <p className="mb-4 text-red-500">{error}</p>}
      <div className="flex space-x-4">
        <button
          onClick={handleLeave}
          disabled={loading}
          className="px-6 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
        >
          {loading ? 'Leaving...' : 'Leave group'}
        </button>
        <button
          onClick={handleCancel}
          className="px-6 py-2 bg-gray-600 rounded-lg hover:bg-gray-500 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

export default LeaveGroup;
