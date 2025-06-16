import type {Driver} from "../types/driver.ts";
import { useNavigate } from "react-router-dom";

const DriverCard = ({driver}: { driver: Partial<Driver> }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (driver.driver_id) {
            navigate(`/driver/${driver.driver_id}`);
        }
    };

    console.log('DriverCard rendered for:', driver.driver_id, 'teamname:', driver.team);

    return (
        <div
            onClick={handleClick}
            className={`bg-f1-black text-f1-white rounded-tr-xl border-t-2 border-r-2 border-f1-white p-2 w-56 font-fregular flex flex-col items-stretch justify-between relative group transition-all duration-300 hover:pt-4 mt-4 hover:mt-2 hover:border-team-${driver.team} cursor-pointer`}
        >
            <div className="flex flex-row justify-between items-center">
                <div className="text-xs text-center flex flex-col">
                    <span className="font-fwide text-base">{driver.points}</span>
                    <span className="bg-f1-white text-f1-black font-fwide text-xs rounded-xl px-2">PTS</span>
                </div>
                <div className="text-4xl font-fbold">{driver.position}</div>
            </div>

            <div className="relative w-full flex justify-center items-center">
                <div className="absolute left-0 top-1/2 -translate-y-1/2 text-8xl font-fregular text-team-mclaren opacity-40 pointer-events-none">
                    {driver.driverNumber}
                </div>
                <img
                    src={`/assets/driver-images/${driver.driver_id}.avif`}
                    alt={driver.surname}
                    className={`w-48 mb-2 p-1 z-10 relative`}
                />
            </div>

            <div className="flex flex-row items-center justify-between w-full px-2">
                <div className="text-xs uppercase tracking-widest mr-2">
                    {driver.forename} <span className="font-fbold text-base">{driver.surname}</span>
                </div>
                <img
                    src={`/assets/nationality-icons/${driver.nationality ?? 'British'}.avif`}
                    alt={driver.nationality}
                    className="w-5 h-4 mt-1 ml-auto border border-f1-white"
                />
            </div>
        </div>
    );
};

export default DriverCard;