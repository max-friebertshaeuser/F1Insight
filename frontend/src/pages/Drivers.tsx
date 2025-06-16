import DriverCard from '../components/DriverCard';
import type {Driver} from "../types/driver.ts";

const demoDriver: Partial<Driver> = {
    id: 'lannor',
    firstName: 'Lando',
    lastName: 'Norris',
    driverNumber: 4,
    country: 'united-kingdom',
    dateOfBirth: '1999-11-13',
    wins: 0,
    podiums: 0,
    polePositions: 0,
    points: 183,
    rank: 1,
    team: 'mclaren',

}



export default function Drivers() {
    return (
        <div className="flex flex-col items-center bg-f1-black justify-center min-h-screen text-white">
            <DriverCard driver={demoDriver}/>
        </div>
    );
}