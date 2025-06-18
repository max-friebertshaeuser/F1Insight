// src/pages/LeaveGroup.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

function LeaveGroup() {
  const [groupName, setGroupName] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLeave = async () => {
    try {
      const res = await fetch(`${API_BASE_GROUPS}/leave/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ group_name: groupName }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.status || json.error);
      navigate('/groups');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white">
      <h1 className="text-4xl font-bold mb-6">Leave Group</h1>
      <input
        type="text"
        value={groupName}
        onChange={e => setGroupName(e.target.value)}
        placeholder="Group Name"
        className="w-full max-w-sm p-2 mb-4 bg-gray-700 rounded"
      />
      <button
        onClick={handleLeave}
        className="w-full max-w-sm p-2 bg-red-600 rounded"
      >
        Leave
      </button>
      {error && <p className="mt-2 text-red-500">{error}</p>}
    </div>
  );
}
export default LeaveGroup;