import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAuthHeaders, API_BASE_BETTING } from '../../utils/api';
import type { Driver } from '../../types/driver';
import DriverCardCompact from '../../components/DriverCardCompact';

interface Race {
  id: string;
  season: string;
  circuit: string;
  date: string;
}

interface BetDetail {
  race: string;
  bet_top_3: string[];
  bet_last_5: string;
  bet_last_10: string;
  bet_fastest_lap: string;
}

export default function RaceBets() {
  const { groupName } = useParams<{ groupName: string }>();
  const [races, setRaces] = useState<Race[]>([]);
  const [bets, setBets] = useState<Record<string, BetDetail | null>>({});
  const [drivers, setDrivers] = useState<Record<string, Driver>>({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);

        const rRes = await fetch(`${API_BASE_BETTING}/available-races/`, {
          headers: getAuthHeaders(),
        });
        const race: Race = await rRes.json();
        setRaces([race]);

        const betMap: Record<string, BetDetail | null> = {};
        for (const rc of [race]) {
          const res = await fetch(`${API_BASE_BETTING}/${rc.id}/show/`, {
            method: 'POST',
            headers: {
              ...getAuthHeaders(),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ group: groupName, race: rc.id }),
          });
          if (res.ok) {
            const json: BetDetail = await res.json();
            betMap[rc.id] = json;
          } else {
            betMap[rc.id] = null;
          }
        }
        setBets(betMap);

        const allDriverIds = new Set<string>();
        Object.values(betMap).forEach(bet => {
          if (!bet) return;
          bet.bet_top_3.forEach(id => allDriverIds.add(id));
          if (bet.bet_last_5) allDriverIds.add(bet.bet_last_5);
          if (bet.bet_last_10) allDriverIds.add(bet.bet_last_10);
          if (bet.bet_fastest_lap) allDriverIds.add(bet.bet_fastest_lap);
        });

        await fetchDriverDetails(Array.from(allDriverIds));
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, [groupName]);

  async function fetchDriverDetails(ids: string[]) {
    const driverMap: Record<string, Driver> = { ...drivers };
    await Promise.all(
      ids.map(async id => {
        if (!driverMap[id]) {
          const res = await fetch(`http://localhost:8000/api/catalog/driver/detailedview`, {
            method: 'POST',
            headers: {
              ...getAuthHeaders(),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ driver_id: id }),
          });
          if (res.ok) {
            const data = await res.json();
            driverMap[id] = data.driver;
          } else {
            console.warn(`Failed to fetch driver ${id}`);
          }
        }
      })
    );
    setDrivers(driverMap);
  }

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading...</p>;

  return (
    <div className="bg-[#0F0F17] text-white min-h-screen py-10 px-4">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold mb-8 text-center">Betting in {groupName}</h2>

        <div className="space-y-6">
          {races.map(race => {
            const bet = bets[race.id];
            return (
              <div key={race.id} className="flex flex-col items-start bg-gray-800 rounded-xl p-6 shadow-lg">
                <div className="w-full flex flex-col sm:flex-row justify-between items-start sm:items-center">
                  <div>
                    <h3 className="text-xl font-semibold">{race.circuit}</h3>
                    <p className="text-gray-400">{race.date} · Season {race.season}</p>
                  </div>

                  <div className="mt-4 sm:mt-0 space-x-2">
                    {!bet ? (
                      <button
                        onClick={() => navigate(`set/${race.id}`)}
                        className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-700 transition"
                      >
                        Place Bet
                      </button>
                    ) : (
                      <>
                        <button
                          onClick={() => navigate(`edit/${race.id}`)}
                          className="px-4 py-2 bg-yellow-600 rounded-lg hover:bg-yellow-700 transition"
                        >
                          Edit Bet
                        </button>
                        <button
                          onClick={() => navigate(`delete/${race.id}`)}
                          className="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition"
                        >
                          Delete Bet
                        </button>
                      </>
                    )}
                  </div>
                </div>

                {bet && (
                  <div className="mt-6 w-full bg-gray-900 rounded-lg p-4">
                    <h4 className="font-medium mb-3 text-center">Your current picks:</h4>

                    <div className="flex flex-wrap justify-evenly gap-6">
                      {/* Top 3 */}
                      {bet.bet_top_3.map((id, idx) => {
                        const driver = drivers[id];
                        return (
                          <div key={`top3-${id}`} className="w-28">
                            {driver ? (
                              <DriverCardCompact driver={driver} label={`Top ${idx + 1}`} />
                            ) : (
                              <div className="text-sm bg-blue-700 px-2 py-1 rounded">
                                Top {idx + 1}: {id}
                              </div>
                            )}
                          </div>
                        );
                      })}

                      {/* Last 5 */}
                      {bet.bet_last_5 && (
                        <div className="w-28">
                          {drivers[bet.bet_last_5] ? (
                            <DriverCardCompact driver={drivers[bet.bet_last_5]} label="Last 5" />
                          ) : (
                            <div className="text-sm bg-indigo-700 px-2 py-1 rounded">Last 5: {bet.bet_last_5}</div>
                          )}
                        </div>
                      )}

                      {/* Last 10 */}
                      {bet.bet_last_10 && (
                        <div className="w-28">
                          {drivers[bet.bet_last_10] ? (
                            <DriverCardCompact driver={drivers[bet.bet_last_10]} label="Last 10" />
                          ) : (
                            <div className="text-sm bg-indigo-500 px-2 py-1 rounded">Last 10: {bet.bet_last_10}</div>
                          )}
                        </div>
                      )}

                      {/* Fastest Lap */}
                      {bet.bet_fastest_lap && (
                        <div className="w-28">
                          {drivers[bet.bet_fastest_lap] ? (
                            <DriverCardCompact driver={drivers[bet.bet_fastest_lap]} label="Fastest" />
                          ) : (
                            <div className="text-sm bg-green-700 px-2 py-1 rounded">Fastest: {bet.bet_fastest_lap}</div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
