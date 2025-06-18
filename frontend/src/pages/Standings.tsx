import { useNavigate } from 'react-router-dom';
import { useDriverStandingsTable } from '../hooks/useDriverStandingsTable';
import { useTeamStandingsTable } from '../hooks/useTeamStandingsTable';

export default function StandingsPage() {
    const navigate = useNavigate();
    const {
        data: drivers,
        loading: loadingDrivers,
        error: errorDrivers,
    } = useDriverStandingsTable();
    const {
        data: teams,
        loading: loadingTeams,
        error: errorTeams,
    } = useTeamStandingsTable();

    if (loadingDrivers || loadingTeams) {
        return <div className="text-f1-white p-8">Loading standings…</div>;
    }
    if (errorDrivers || errorTeams || !drivers || !teams) {
        return <div className="text-f1-red p-8">Error loading standings data.</div>;
    }
    console.log('Drivers Standings:', drivers);
    return (
        <div className="p-8 px-96 space-y-12 bg-f1-black text-f1-white font-fregular">
            {/* Drivers Standings */}
            <section>
                <h2 className="text-3xl font-fwide mb-4">Drivers Standings</h2>
                <table className="min-w-full bg-gray-800 rounded-lg overflow-hidden table-auto">
                    <thead className="bg-gray-700">
                    <tr>
                        <th className="p-2">Pos</th>
                        <th className="p-2 text-left">Driver</th>
                        <th className="p-2 text-left">Team</th>
                        <th className="p-2">Pts</th>
                    </tr>
                    </thead>
                    <tbody>
                    {drivers.map((d) => (
                        <tr
                            key={d.driver}
                            className="hover:bg-gray-700 cursor-pointer"
                            onClick={() =>
                                navigate(`/driver/${encodeURIComponent(d.driver_id)}`)
                            }
                        >
                            <td className="p-2 text-center">{d.position}</td>
                            <td className="p-2 flex items-center space-x-2">
                                <img
                                    src={`/assets/nationality-icons/${d.nationality}.avif`}
                                    alt={d.nationality}
                                    className="w-5 h-4 border border-white"
                                />
                                <span>{d.driver}</span>
                            </td>
                            <td className="p-2 text-left">{d.team}</td>
                            <td className="p-2 text-center font-fbold">{d.points}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </section>

            <div className="h-24"/>

            {/* Teams Standings */}
            <section>
                <h2 className="text-3xl font-fwide mb-4">Teams Standings</h2>
                <table className="min-w-full bg-gray-800 rounded-lg overflow-hidden">
                    <thead className="bg-gray-700">
                    <tr>
                        <th className="p-2">Pos</th>
                        <th className="p-2 text-left">Team</th>
                        <th className="p-2">Pts</th>
                    </tr>
                    </thead>
                    <tbody>
                    {teams.map((t) => {
                        return (
                            <tr
                                key={t.team}
                                className="hover:bg-gray-700 cursor-pointer"
                                onClick={() => navigate(`/team/${encodeURIComponent(t.team_id)}`)}
                            >
                                <td className="p-2 text-center">{t.position}</td>
                                <td className="p-2 flex items-center space-x-2">
                                    <img
                                        src={`/assets/team-images/${t.team_id}.avif`}
                                        alt={t.team}
                                        className="w-6 h-6"
                                    />
                                    <span>{t.team}</span>
                                </td>
                                <td className="p-2 text-center font-fbold">{t.points}</td>
                            </tr>
                        );
                    })}
                    </tbody>
                </table>
            </section>
        </div>
    );
}
