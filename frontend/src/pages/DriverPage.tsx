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
    const [season, setSeason] = useState(new Date().getFullYear()); // default to current season

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
                console.log('Fetched driver details:', data.driver);
                data.driver.current_team = getTeamClass(data.driver.current_team ?? '');
                setDriver(data.driver);
            } catch (err) {
                console.error('Failed to fetch driver details:', err);
            }
        };

        fetchDriver();
    }, [id]);

    if (!driver) return <div className="text-f1-white p-8">Loading...</div>;

    console.log('Driver details:', driver);

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
        <section
            className="min-h-screen w-screen bg-f1-black text-f1-white font-fregular p-8 pt-20 flex flex-col items-center overflow-x-hidden">
            <h1 className="text-5xl font-fwide text-right px-8 md:px-64">
                <span className="block text-left">{driver.forename}</span>
                <span
                    className={`text-8xl font-fwide text-white text-right drop-shadow-team-${driver.current_team} drop-shadow-xl `}>{driver.surname}</span>
            </h1>

            <div
                className="mt-8 flex flex-col md:flex-row justify-center md:justify-between md:w-5/6 items-center gap-16 pb-8">
                <div className="relative flex justify-center px-4">
                    <img
                        src={`/assets/driver-images/${driver.driver_id}.avif`}
                        alt={driver.surname}
                        className="w-128 z-20"
                    />
                    <div
                        className={`absolute left-0 bottom-1/6 -translate-y-1/2 text-9xl font-fregular  text-team-${driver.current_team} opacity-40 pointer-events-none z-10`}>
                        {driver.current_number ?? '06'}
                    </div>
                    <div
                        className={`absolute bottom-0 w-full h-1/5 bg-transparent rounded-br-xl border-b-2 border-r-2 drop-shadow-team-${driver.current_team} drop-shadow-xl z-30`}
                    />
                </div>


                <div className="grid grid-cols-[1fr_auto_1fr] gap-4 text-xl font-fwide items-center">
                    <div className="pr-4">
                        <h2 className="text-2xl border-f1-white inline-block mb-4 text-left">Overall</h2>
                        {overallStats.map((stat) => (
                            <div key={stat.label} className="grid grid-cols-[2fr_1fr] gap-8 mb-4">
                                <span
                                    className={`text-4xl text-team-${driver.current_team} text-right`}>{stat.value}</span>
                                <span className="text-white/80 text-left font-fregular">{stat.label}</span>
                            </div>
                        ))}
                    </div>

                    <div className="h-full border-r border-f1-white mx-auto w-px"/>

                    <div className="text-left pl-4">
                        <h2 className="text-2xl border-f1-white inline-block mb-4">Current</h2>
                        {currentStats.map((stat) => (
                            <div key={stat.label} className="grid grid-cols-2 gap-8 mb-4">
                                <span
                                    className={`text-4xl text-team-${driver.current_team} text-right`}>{stat.value}</span>
                                <span className="text-white/80 text-left font-fregular">{stat.label}</span>
                            </div>
                        ))}
                    </div>
                </div>


            </div>


            <div className="h-48"/>
            {/* Spacer */}

            <h2 className="text-5xl font-fwide text-right px-8 md:px-64 w-full mb-8">
                <span className="block text-left">Season</span>
                <span
                    className={`text-8xl font-fwide text-white text-right drop-shadow-team-${driver.current_team} drop-shadow-xl`}>
    Performance
  </span>
            </h2>

            <section className="w-full flex flex-col justify-center items-center">
                <div className="border-b-2">
                    <CustomGraph
                        driverId={driver.driver_id}
                        height={600}
                        width={1200}
                        team={driver.current_team}
                        season={season}
                    />
                </div>

                <div className="w-full flex justify-center">
                    <div className="w-[1200px] overflow-x-auto scrollbar-thin">
                        <div className="flex gap-4 mb-4  min-w-fit">
                            {driver.seasons_active.map((yr) => (
                                <Button key={yr} active={season === yr} onClick={() => setSeason(yr)}>
                                    {yr}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>
            </section>


            <section
                className="min-h-screen w-full bg-f1-black text-f1-white font-fregular p-8 pt-32 flex flex-col items-center">
                <h2 className="text-5xl font-fwide text-right px-8 md:px-64 w-full mb-8">
                    <span className="block text-left">Season</span>
                    <span className="text-8xl font-fwide text-white text-right drop-shadow-xl">
      Comparison
    </span>
                </h2>



                <div className="w-[1200px]">
                    <CustomBoxplot
                        driverId={driver.driver_id}
                        team={driver.current_team}
                        width={1200}
                        height={600}
                    />

                </div>
            </section>


        </section>


    );
};

export default DriverPage;
