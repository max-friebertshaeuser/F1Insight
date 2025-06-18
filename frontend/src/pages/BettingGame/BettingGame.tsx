// src/pages/BettingGame.tsx
import React from 'react';
import { Link } from 'react-router-dom';

function BettingGame() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F0F17] text-white">
      <h1 className="text-4xl font-bold mb-6">Formula 1 Tippspiel</h1>
      <nav className="space-y-2">
        <Link to="/groups/create" className="block p-2 bg-blue-600 rounded">Gruppe erstellen</Link>
        <Link to="/groups/join" className="block p-2 bg-blue-600 rounded">Gruppe beitreten</Link>
        <Link to="/groups" className="block p-2 bg-blue-600 rounded">Meine Gruppen</Link>
        <Link to="/groups/leave" className="block p-2 bg-blue-600 rounded">Gruppe verlassen</Link>
        <Link to="/bets/create" className="block p-2 bg-green-600 rounded">Wette platzieren</Link>
        <Link to="/bets/bottom5-before" className="block p-2 bg-gray-600 rounded">Bottom 5 (vor Wahl)</Link>
        <Link to="/bets/bottom5-after" className="block p-2 bg-gray-600 rounded">Bottom 5 (nach Wahl)</Link>
      </nav>
    </div>
  );
}
export default BettingGame;
