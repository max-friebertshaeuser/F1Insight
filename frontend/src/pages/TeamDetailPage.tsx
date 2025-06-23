import {useParams} from 'react-router-dom';
import {useEffect, useState} from 'react';
import {getTeamClass} from "../utils/formatTeamClass.ts";
import CustomGraph from "../components/CustomGraph.tsx";
import Button from "../components/Button.tsx";
import CustomBoxplot from "../components/CustomBoxplot.tsx";

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
        season: number;
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
    seasons_active: number[];
}

const TeamDetailPage = () => {
    const {id} = useParams();
    const [data, setData] = useState<TeamData | null>(null);
    const [season, setSeason] = useState(new Date().getFullYear()); // default to current season

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
        <>
            <section
                className="min-h-screen w-screen bg-f1-black text-f1-white font-fregular p-8 pt-20 flex flex-col items-center overflow-x-hidden">
                <h1 className="text-3xl md:text-5xl font-fwide text-center px-8 md:px-64 mb-4">
                    <span className="block text-left">Team</span>
                    <span
                        className={`text-5xl md:text-8xl font-fwide text-white text-right drop-shadow-xl drop-shadow-team-${teamColorClass}`}>{data.team.name}
                </span>

                </h1>

                <div className="flex flex-col md:flex-row justify-center items-start md:items-center gap-16 pb-8 mt-8">
                    {/* Driver Card */}
                    <div className="relative flex flex-col items-center px-4 w-full md:w-auto">
                        {/* Driver images with overlap */}
                        <div className="relative flex justify-center w-full">
                            <div className="flex -space-x-32 z-10">
                                {data.current_season.drivers?.slice(0, 2).map((d) => (
                                    <img
                                        key={d.id}
                                        src={`/assets/driver-images/${d.id}.avif`}
                                        alt={`${d.forename} ${d.surname}`}
                                        className="w-56 p-1 relative drop-shadow-md md:drop-shadow-lg md:w-86"
                                    />
                                ))}
                            </div>

                            {/* Stylish bottom bar */}
                            <div
                                className={`absolute bottom-0 w-full h-1/5 bg-transparent rounded-br-xl border-b-2 border-r-2 drop-shadow-team-${teamColorClass} drop-shadow-xl z-20`}
                            />
                        </div>

                        {/* Names + logo */}
                        <div className="w-full flex justify-between items-center px-2 mt-4 z-30">
                            <div className="text-2xl font-fbold">
                                {data.current_season.drivers.slice(0, 2).map((d) => (
                                    <div key={d.id}>
                                        <span className="text-base font-fregular">{d.forename}</span> {d.surname}
                                    </div>
                                ))}
                            </div>
                            <img
                                src={`/assets/team-images/${data.team.id}.avif`}
                                alt={data.team.name}
                                className="w-10 h-10 ml-auto border border-f1-white"
                            />
                        </div>
                    </div>

                    {/* Stats */}
                    <div className="flex flex-col md:grid md:grid-cols-[1fr_auto_1fr] gap-4 text-xl font-fwide items-start w-full md:w-auto">
                        {/* Overall Stats */}
                        <div className="pr-4 w-full">
                            <h2 className="text-2xl border-f1-white inline-block mb-4 text-left">Overall</h2>
                            {overallStats.map((stat) => (
                                <div key={stat.label} className="grid grid-cols-[2fr_1fr] gap-8 mb-4">
                                    <span className={`text-3xl text-f1-white/90 text-right text-team-${teamColorClass}`}>{stat.value}</span>
                                    <span className="text-white/80 text-left font-fregular text-sm md:text-base">{stat.label}</span>
                                </div>
                            ))}
                        </div>

                        {/* Divider */}
                        <div className="w-full h-px border-t border-f1-white my-4 md:border-r md:border-t-0 md:my-0 md:mx-auto md:h-full md:w-px md:mr-8" />

                        {/* Current Stats */}
                        <div className=" w-full">
                            <h2 className="text-2xl border-f1-white inline-block mb-4 text-left">Current</h2>
                            {currentStats.map((stat) => (
                                <div key={stat.label} className="grid grid-cols-[2fr_1fr] gap-8 mb-4">
                                    <span className={`text-3xl text-f1-white/90 text-right text-team-${teamColorClass}`}>{stat.value}</span>
                                    <span className="text-white/80 text-left font-fregular text-sm md:text-base">{stat.label}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </section>
            <section className="w-full flex flex-col justify-center items-center mt-32 md:px-32 mx-auto">
                <h2 className="text-xl font-fwide text-right px-8 md:px-96 w-full  md:text-4xl">
                    <span className="block text-left">Season</span>
                    <span className={`text-2xl font-fwide text-white text-right drop-shadow-lg drop-shadow-team-${teamColorClass} md:text-6xl `}>
                        Performance
                    </span>
                </h2>

                <div className="w-full overflow-x-auto border-b-2 md:mx-auto md:px-32 md:flex justify-center items-center">
                    <div className="w-[1200px]">
                        <CustomGraph
                            driverId={data.current_season.drivers[0]?.id}
                            driverId2={data.current_season.drivers[1]?.id}
                            height={600}
                            width={1200}
                            team={getTeamClass(data.team.name)}
                            team2={getTeamClass(data.team.name)}
                            season={season}
                            driverName={data.current_season.drivers[0]?.surname}
                            driverName2={data.current_season.drivers[1]?.surname}
                        />
                    </div>
                </div>


                <div className="w-full flex justify-center">
                    <div className="w-[1200px] overflow-x-auto scrollbar-thin">
                        <div className="flex gap-4 mb-4 min-w-fit">
                            {data.seasons_active.map((yr) => (
                                <Button key={yr} active={season === yr} onClick={() => setSeason(yr)}>
                                    {yr}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            <section className="w-full flex flex-col justify-center items-center mt-48 md:px-32 mx-auto">
                <h2 className="text-xl font-fwide text-right px-8 md:px-96 w-full md:text-4xl">
                    <span className="block text-left">Season</span>
                    <span
                        className={`text-2xl font-fwide text-white text-right drop-shadow-lg drop-shadow-team-${teamColorClass} md:text-6xl`}
                    >
      Consistency
    </span>
                </h2>

                <div className="w-full overflow-x-auto pt-20 md:mx-auto md:px-32 md:flex justify-center items-center">
                    <div className="w-[1200px]">
                        <CustomBoxplot
                            driverId={data.current_season.drivers[0]?.id}
                            driverId2={data.current_season.drivers[1]?.id}
                            team={data.team.id}
                            team2={data.team.id /* or a secondary variant if desired */}
                            width={1200}
                            height={600}
                            driverName={data.current_season.drivers[0]?.surname}
                            driverName2={data.current_season.drivers[1]?.surname}
                        />
                    </div>
                </div>
            </section>



        </>


);
};

export default TeamDetailPage;