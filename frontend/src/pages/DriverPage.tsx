import {useParams} from 'react-router-dom';
import {useEffect, useState} from 'react';
import {getTeamClass} from "../utils/formatTeamClass.ts";
import CustomGraph from "../components/CustomGraph.tsx";
import Button from "../components/Button.tsx";
import CustomBoxplot from "../components/CustomBoxplot.tsx";

interface DriverDetails {
    driver_id: string;
    forename: string;
    surname: string;
    current_number: number;
    current_team: string;
    date_of_birth: string;
    place_of_birth: string;
    career_wins: number;
    career_points: number;
    career_podiums: number;
    career_poles: number;
    grand_prix_entered: number;
    world_championships: number;
    best_grid_position: number;
    current_season_points: number;
    current_season_wins: number;
    current_season_podiums: number;
    current_season_poles: number;
    seasons_active: number[]
}

const DriverPage = () => {
    const {id} = useParams();
    const [driver, setDriver] = useState<DriverDetails | null>(null);
    const [season, setSeason] = useState(new Date().getFullYear());

    useEffect(() => {
        const fetchDriver = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/catalog/driver/detailedview`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({driver_id: id})
                });

                const data = await res.json();
                data.driver.driver_id = id;
                data.driver.current_team = getTeamClass(data.driver.current_team ?? '');
                setDriver(data.driver);
            } catch (err) {
                console.error('Failed to fetch driver details:', err);
            }
        };

        fetchDriver();
    }, [id]);

    if (!driver) return <div className="text-f1-white p-8">Loading...</div>;

    const overallStats = [
        {label: "Wins", value: driver.career_wins},
        {label: "Points", value: driver.career_points},
        {label: "Podiums", value: driver.career_podiums},
        {label: "Poles", value: driver.career_poles},
    ];

    const currentStats = [
        {label: "Wins", value: driver.current_season_wins},
        {label: "Points", value: driver.current_season_points},
        {label: "Podiums", value: driver.current_season_podiums},
        {label: "Poles", value: driver.current_season_poles},
    ];

    return (
        <section className="min-h-screen w-screen bg-f1-black text-f1-white font-fregular p-8 pt-20 flex flex-col items-center overflow-x-hidden">
            {/* Header */}
            <h1 className="text-3xl md:text-5xl font-fwide text-center px-8 md:px-64 mb-4">
                <span className="block text-left">{driver.forename}</span>
                <span className={`text-5xl md:text-8xl font-fwide text-white text-right drop-shadow-xl drop-shadow-team-${driver.current_team}`}>
                    {driver.surname}
                </span>
            </h1>

            {/* Driver Image + Stats */}
            <div className="flex flex-col md:flex-row justify-center items-start md:items-center gap-16 pb-8 mt-8">
                <div className="relative flex justify-center px-4 w-full md:w-auto">
                    <img
                        src={`/assets/driver-images/${driver.driver_id}.avif`}
                        alt={driver.surname}
                        className="w-64 md:w-96 z-20"
                    />
                    <div className={`absolute left-0 bottom-1/6 -translate-y-1/2 text-9xl font-fregular text-team-${driver.current_team} opacity-40 pointer-events-none z-10`}>
                        {driver.current_number ?? '06'}
                    </div>
                    <div className={`absolute bottom-0 w-full h-1/5 bg-transparent rounded-br-xl border-b-2 border-r-2 drop-shadow-team-${driver.current_team} drop-shadow-xl z-30`} />
                </div>

                <div className="flex flex-col md:grid md:grid-cols-[1fr_auto_1fr] gap-4 text-xl font-fwide items-start w-full md:w-auto">
                    <div className="pr-4 w-full">
                        <h2 className="text-2xl border-f1-white inline-block mb-4 text-left">Overall</h2>
                        {overallStats.map((stat) => (
                            <div key={stat.label} className="grid grid-cols-[2fr_1fr] gap-8 mb-4">
                                <span className={`text-3xl text-team-${driver.current_team} text-right`}>{stat.value}</span>
                                <span className="text-white/80 text-left font-fregular text-sm md:text-base">{stat.label}</span>
                            </div>
                        ))}
                    </div>
                    <div className="w-full h-px border-t border-f1-white my-4 md:border-r md:border-t-0 md:my-0 md:mx-auto md:h-full md:w-px" />
                    <div className="pl-4 w-full">
                        <h2 className="text-2xl border-f1-white inline-block mb-4 text-left">Current</h2>
                        {currentStats.map((stat) => (
                            <div key={stat.label} className="grid grid-cols-[2fr_1fr] gap-8 mb-4">
                                <span className={`text-3xl text-team-${driver.current_team} text-right`}>{stat.value}</span>
                                <span className="text-white/80 text-left font-fregular text-sm md:text-base">{stat.label}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Performance Section */}
            <section className="w-full flex flex-col justify-center items-center mt-32 md:px-32 mx-auto">
                <h2 className="text-xl font-fwide text-right px-8 md:px-96 w-full md:text-4xl">
                    <span className="block text-left">Season</span>
                    <span className={`text-2xl md:text-6xl font-fwide text-white text-right drop-shadow-lg drop-shadow-team-${driver.current_team}`}>
                        Performance
                    </span>
                </h2>

                <div className="w-full overflow-x-auto border-b-2 md:mx-auto md:px-32 md:flex justify-center items-center">
                    <div className="w-[1200px]">
                        <CustomGraph
                            driverId={driver.driver_id}
                            height={600}
                            width={1200}
                            team={driver.current_team}
                            season={season}
                            driverName={driver.surname}
                        />
                    </div>
                </div>

                <div className="w-full flex justify-center">
                    <div className="w-[1200px] overflow-x-auto scrollbar-thin">
                        <div className="flex gap-4 mb-4 min-w-fit">
                            {driver.seasons_active.map((yr) => (
                                <Button key={yr} active={season === yr} onClick={() => setSeason(yr)}>
                                    {yr}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* Consistency Section */}
            <section className="w-full flex flex-col justify-center items-center mt-48 md:px-32 mx-auto">
                <h2 className="text-xl font-fwide text-right px-8 md:px-96 w-full md:text-4xl">
                    <span className="block text-left">Season</span>
                    <span className={`text-2xl md:text-6xl font-fwide text-white text-right drop-shadow-lg drop-shadow-team-${driver.current_team}`}>
                        Comparison
                    </span>
                </h2>

                <div className="w-full overflow-x-auto  md:mx-auto md:px-32 md:flex justify-center items-center">
                    <div className="w-[1200px]">
                        <CustomBoxplot
                            driverId={driver.driver_id}
                            team={driver.current_team}
                            width={1200}
                            height={600}
                            driverName={driver.surname}
                        />
                    </div>
                </div>
            </section>
        </section>
    );
};

export default DriverPage;

