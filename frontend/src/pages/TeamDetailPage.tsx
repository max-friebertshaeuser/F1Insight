import {useParams} from 'react-router-dom';
import {useEffect, useState} from 'react';
import {getTeamClass} from "../utils/formatTeamClass.ts";
import teamsPage from "./TeamsPage.tsx";
import teamCard from "../components/TeamCard.tsx";

interface DriverSummary {
    id: string;
    forename: string;
    surname: string;
    number: string;
}

interface TeamDetails {
    id: string;
    name: string;
    nationality: string;
}

interface TeamData {
    team: TeamDetails;
    current_season: {
        season: string;
        drivers: DriverSummary[];
        wins: number;
        points: number;
        podiums: number;
        poles: number;
    };
    career: {
        wins: number;
        points: number;
        podiums: number;
        poles: number;
    };
}

const TeamDetailPage = () => {
    const {id} = useParams();
    const [data, setData] = useState<TeamData | null>(null);

    useEffect(() => {
        const fetchTeam = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/catalog/team/detailedview
`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json',
                    },
                    body: JSON.stringify({team_id: id}),
                });

                const json = await res.json();
                setData(json);
            } catch (err) {
                console.error('Failed to fetch team details:', err);
            }
        };

        fetchTeam();
    }, [id]);

    if (!data) return <div className="text-f1-white p-8">Loading...</div>;

    const overallStats = [
        {label: 'Wins', value: data.career.wins},
        {label: 'Points', value: data.career.points},
        {label: 'Podiums', value: data.career.podiums},
        {label: 'Poles', value: data.career.poles},
    ];

    const currentStats = [
        {label: 'Wins', value: data.current_season.wins},
        {label: 'Points', value: data.current_season.points},
        {label: 'Podiums', value: data.current_season.podiums},
        {label: 'Poles', value: data.current_season.poles},
    ];

    const teamColorClass = getTeamClass(data.team.name);


    return (
        <section
            className="min-h-screen w-screen bg-f1-black text-f1-white font-fregular p-8 pt-20 flex flex-col items-center overflow-x-hidden">
            <h1 className="text-5xl font-fwide text-center px-8 md:px-64 mb-4">
                <span className="block text-left">Team</span>
                <span
                    className={`text-8xl font-fwide text-white text-right drop-shadow-xl drop-shadow-team-${teamColorClass}`}>{data.team.name}</span>
            </h1>

            <div className="flex flex-col md:flex-row justify-center items-center gap-16 pb-8 mt-8">
                <div className="relative flex justify-center px-4">
                    <div className="flex -space-x-56">
                        {data.current_season.drivers?.slice(0, 2).map((d) => (
                            <img
                                key={d.id}
                                src={`/assets/driver-images/${d.id}.avif`}
                                alt={`${d.forename} ${d.surname}`}
                                className="w-128 p-1 z-10 relative drop-shadow-md "
                            />
                        ))}
                    </div>
                    <div
                        className={`absolute bottom-0 w-full h-1/5 bg-transparent rounded-br-xl border-b-2 border-r-2 drop-shadow-team-${teamColorClass} drop-shadow-xl z-30`}
                    />
                </div>

                <div className="grid grid-cols-[1fr_auto_1fr] gap-4 text-xl font-fwide items-center">
                    <div className="pr-4">
                        <h2 className="text-2xl border-f1-white inline-block mb-4 text-left">Overall</h2>
                        {overallStats.map((stat) => (
                            <div key={stat.label} className="grid grid-cols-[2fr_1fr] gap-8 mb-4">
                                <span
                                    className={`text-4xl text-f1-white/90 text-right text-team-${teamColorClass}`}>{stat.value}</span>
                                <span className="text-white/80 text-left font-fregular">{stat.label}</span>
                            </div>
                        ))}
                    </div>

                    <div className="h-full border-r border-f1-white mx-auto w-px"/>

                    <div className="text-left pl-4">
                        <h2 className="text-2xl border-f1-white inline-block mb-4">Current</h2>
                        {currentStats.map((stat) => (
                            <div key={stat.label} className="grid grid-cols-2 gap-8 mb-4">
                                <span className={`text-4xl text-f1-white/90 text-right text-team-${teamColorClass}`}>
                                    {stat.value}
                                </span>
                                <span className="text-white/80 text-left font-fregular">{stat.label}</span>
                            </div>
                        ))}
                    </div>
                </div>


            </div>
        </section>
    );
};

export default TeamDetailPage;