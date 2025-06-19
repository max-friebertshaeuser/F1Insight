// src/pages/BettingGame.tsx
import React from 'react';
import { Link } from 'react-router-dom';

function BettingGame() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white">
      <h1 className="text-4xl font-bold mb-6">Formula 1 Betting Game</h1>
      <nav className="space-y-2">
        <Link to="/groups" className="block p-2 bg-blue-600 rounded">Betting Groups</Link>
      </nav>
    </div>
  );
}
export default BettingGame;
