import { useNavigate } from "react-router-dom";

interface DriverSummary {
    driver_id: string;
    forename: string;
    surname: string;
}

export interface Team {
    team_id: string;
    name: string;
    points: number;
    position: number;
    type: string;
    drivers?: DriverSummary[];
}

const TeamCard = ({ team }: { team: Partial<Team> }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (team.team_id) {
            navigate(`/team/${team.team_id}`);
        }
    };

    return (
        <div
            onClick={handleClick}
            className={`bg-f1-black text-f1-white rounded-tr-xl border-t-2 border-r-2 border-f1-white p-2 w-96 font-fregular flex flex-col items-stretch justify-between relative group transition-all duration-300 hover:pt-4 mt-4 hover:mt-2 hover:border-team-${team.name} cursor-pointer`}
        >
            <div className="flex flex-row justify-between items-center">
                <div className="text-xs text-center flex flex-col">
                    <span className="font-fwide text-base">{team.points}</span>
                    <span className="bg-f1-white text-f1-black font-fwide text-xs rounded-xl px-2">PTS</span>
                </div>
                <div className="text-4xl font-fbold">{team.position}</div>
            </div>

            <div className="relative w-full flex justify-center items-center mb-2">
                <div className="flex -space-x-16">
                    {team.drivers?.slice(0, 2).map((d) => (
                        <img
                            key={d.driver_id}
                            src={`/assets/driver-images/${d.driver_id}.avif`}
                            alt={`${d.forename} ${d.surname}`}
                            className={`w-48 mb-2 p-1 z-10 relative`}
                        />
                    ))}
                </div>
            </div>

            <div className="flex flex-col items-start w-full px-2">
                <div className="text-xs uppercase tracking-widest font-fbold text-base">
                    {team.name}
                </div>
                <div className="text-xs mb-1 italic text-f1-lightgray">
                    {team.type}
                </div>
                <div className="text-xs">
                    {team.drivers?.slice(0, 2).map((d) => (
                        <div key={d.driver_id}>{d.forename} {d.surname}</div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default TeamCard;