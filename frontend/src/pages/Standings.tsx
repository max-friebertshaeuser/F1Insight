import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface DriverStanding {
    pos: number;
    driverId: string;
    fullName: string;
    nationality: string;
    team: string;
    points: number;
}

interface ConstructorStanding {
    pos: number;
    teamId: string;
    teamName: string;
    points: number;
}

export default function StandingsPage() {
    const [drivers, setDrivers] = useState<DriverStanding[]>([]);
    const [constructors, setConstructors] = useState<ConstructorStanding[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        // Replace with your real API or capture these standings
        setDrivers([
            { pos: 1, driverId: 'piastri', fullName: 'Oscar Piastri', nationality: 'AUS', team: 'McLaren', points: 198 },
            { pos: 2, driverId: 'norris', fullName: 'Lando Norris', nationality: 'GBR', team: 'McLaren', points: 176 },
            { pos: 3, driverId: 'verstappen', fullName: 'Max Verstappen', nationality: 'NED', team: 'Red Bull Racing', points: 155 },
            { pos: 4, driverId: 'russell', fullName: 'George Russell', nationality: 'GBR', team: 'Mercedes', points: 136 },
        ]);

        setConstructors([
            { pos: 1, teamId: 'mclaren', teamName: 'McLaren', points: 374 },
            { pos: 2, teamId: 'mercedes', teamName: 'Mercedes', points: 199 },
            { pos: 3, teamId: 'ferrari', teamName: 'Ferrari', points: 183 },
            { pos: 4, teamId: 'redbull', teamName: 'Red Bull Racing', points: 162 },
        ]);
    }, []);

    return (
        <div className="p-8 space-y-12 bg-f1-black text-f1-white font-fregular">
            <section>
                <h2 className="text-3xl font-fwide mb-4">Drivers Standings</h2>
                <table className="min-w-full bg-gray-800 rounded-lg overflow-hidden">
                    <thead className="bg-gray-700">
                    <tr>
                        <th className="p-2">Pos</th>
                        <th className="p-2">Driver</th>
                        <th className="p-2">Team</th>
                        <th className="p-2">Pts</th>
                    </tr>
                    </thead>
                    <tbody>
                    {drivers.map(d => (
                        <tr key={d.pos} className="hover:bg-gray-700 cursor-pointer"
                            onClick={() => navigate(`/driver/${d.driverId}`)}>
                            <td className="p-2 text-center">{d.pos}</td>
                            <td className="p-2 flex items-center space-x-2">
                                <img
                                    src={`/assets/nationality-icons/${d.nationality}.avif`}
                                    alt={d.nationality}
                                    className="w-5 h-4 border border-white"
                                />
                                <span>{d.fullName}</span>
                            </td>
                            <td className="p-2">{d.team}</td>
                            <td className="p-2 text-right font-fbold">{d.points}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </section>

            <section>
                <h2 className="text-3xl font-fwide mb-4">Teams Standings</h2>
                <table className="min-w-full bg-gray-800 rounded-lg overflow-hidden">
                    <thead className="bg-gray-700">
                    <tr>
                        <th className="p-2">Pos</th>
                        <th className="p-2">Team</th>
                        <th className="p-2">Pts</th>
                    </tr>
                    </thead>
                    <tbody>
                    {constructors.map(t => (
                        <tr key={t.pos} className="hover:bg-gray-700 cursor-pointer"
                            onClick={() => navigate(`/team/${t.teamId}`)}>
                            <td className="p-2 text-center">{t.pos}</td>
                            <td className="p-2 flex items-center space-x-2">
                                <img
                                    src={`/assets/team-logos/${t.teamId}.avif`}
                                    alt={t.teamName}
                                    className="w-6 h-6"
                                />
                                <span>{t.teamName}</span>
                            </td>
                            <td className="p-2 text-right font-fbold">{t.points}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </section>
        </div>
    );
}
