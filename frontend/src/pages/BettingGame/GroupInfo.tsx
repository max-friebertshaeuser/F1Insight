// src/pages/GroupInfo.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getAuthHeaders, API_BASE_GROUPS } from '../../utils/api';

function GroupInfo() {
  const { groupId } = useParams();
  const [info, setInfo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE_GROUPS}/getgroupinfo/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ group_id: parseInt(groupId) }),
    })
      .then(r => r.json())
      .then(data => setInfo(data))
      .catch(e => setError(e.message));
  }, [groupId]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!info) return <p>Loading...</p>;

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-4">{info.group_name}</h2>
      <p><strong>Owner:</strong> {info.owner}</p>
      <h3 className="text-2xl font-bold mt-6 mb-2">Members</h3>
      <ul className="list-disc ml-6 mb-6">
        {info.bet_stats.map(bs => (
          <li key={bs.user}>{bs.user} - {bs.points} points</li>
        ))}
      </ul>
    </div>
  );
}
export default GroupInfo;