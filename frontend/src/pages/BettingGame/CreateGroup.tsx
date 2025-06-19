import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_BASE_GROUPS, getAuthHeaders } from "../../utils/api";

function CreateGroup() {
  const [groupName, setGroupName] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const username = localStorage.getItem('username');
      const res = await fetch(`${API_BASE_GROUPS}/create/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ name: username, group_name: groupName }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.status || json.error || 'Error');
      navigate('/bettinggame');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white">
      <h1 className="text-4xl font-bold mb-6">Create Group</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-sm">
        <input
          type="text"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          placeholder="Group Name"
          className="w-full p-2 mb-4 rounded bg-gray-700"
          required
        />
        <button type="submit" className="w-full p-2 bg-blue-600 rounded">Create</button>
        {error && <p className="mt-2 text-red-500">{error}</p>}
      </form>
    </div>
  );
}
export default CreateGroup;