// src/pages/DeleteBet.jsx
import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

function DeleteBet() {
  const { race_id } = useParams();
  const navigate = useNavigate();

  const handleDelete = async () => {
    await fetch(`${API_BASE_BETTING}/${race_id}/delete/`, { method: 'DELETE', headers: getAuthHeaders() });
    navigate('/groups');
  };

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-4">Delete Bet</h2>
      <button onClick={handleDelete} className="p-2 bg-red-600 rounded">Confirm</button>
    </div>
  );
}
export default DeleteBet;