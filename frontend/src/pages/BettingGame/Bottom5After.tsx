// src/pages/Bottom5After.jsx
import React, { useState, useEffect } from 'react';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';

function Bottom5After() {
  const [drivers, setDrivers] = useState([]);
  useEffect(() => {
    fetch(`${API_BASE_BETTING}/standings/bottom5-after-choice/`, { headers: getAuthHeaders() })
      .then(r => r.ok ? r.json() : Promise.reject('Load failed'))
      .then(data => setDrivers(data))
      .catch(console.error);
  }, []);

  return (
    <div className="p-6 bg-[#0F0F17] text-white min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Bottom 5 After Choice</h2>
      <ul className="list-disc ml-6">
        {drivers.map(d => <li key={d.driver}>{d.driver} ({d.position})</li>)}
      </ul>
    </div>
  );
}
export default Bottom5After;