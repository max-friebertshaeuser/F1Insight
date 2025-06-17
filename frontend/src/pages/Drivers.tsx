import {useEffect, useState} from 'react';
import type {Driver} from "../types/driver.ts";
import DriverCard from "../components/DriverCard.tsx";
import {getTeamClass} from "../utils/formatTeamClass.ts";


// const demoDriver: Partial<Driver> = {
//     driver_id: 'lannor',
//     firstName: 'Lando',
//     lastName: 'Norris',
//     driverNumber: 4,
//     country: 'united-kingdom',
//     dateOfBirth: '1999-11-13',
//     wins: 0,
//     podiums: 0,
//     polePositions: 0,
//     points: 183,
//     rank: 1,
//     team: 'mclaren',
//
// }
const DriversPage = () => {
    const [drivers, setDrivers] = useState<Partial<Driver>[]>([]);

    useEffect(() => {
        const fetchDrivers = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/catalog/getcurrentdrivers', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({}) // send a real payload if needed
                });

                let data: Partial<Driver>[] = (await res.json())['drivers'];
                console.log('Fetched drivers:', data);
                data = data.map(driver => {
                    driver.team = getTeamClass(driver.team ?? '');
                    driver.driverNumber = (driver as any)['number'];
                    return driver;

                }).sort((a, b) => (a.position ?? 0) - (b.position ?? 0));
                console.log('Processed drivers:', data);
                setDrivers(data);
            } catch (err) {
                console.error('Failed to fetch drivers:', err);
            }


            // For now, populate with 20 cloned Lando Norris objects
            // const fakeDrivers: Driver[] = Array.from({length: 20}, (_, i) => ({
            //     ...demoDriver,
            //     id: 'lannor',
            //     rank: i + 1,
            //     points: 183 - i * 2, // Just some descending points for flair
            // } as Driver));
            // setDrivers(fakeDrivers);
        };

        fetchDrivers();
    }, []);

    const firstRow = drivers.slice(0, 3);
    const restRows = drivers.slice(3);

    return (
        <div className="overflow-auto min-h-screen bg-f1-black text-f1-white font-fregular p-4 flex justify-center">
            <div className="w-full max-w-7xl">
                <div className="grid grid-cols-1 sm:grid-cols-3 md:grid-cols-3 gap-8 mb-16 px-16">
                    {firstRow.map(driver => (
                        <div key={driver.driver_id! + driver.position!} className="flex justify-center">
                            <DriverCard driver={driver}/>
                        </div>
                    ))}
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-8">
                    {restRows.map(driver => (
                        <div key={driver.driver_id! + driver.position!} className="flex justify-center mb-8">
                            <DriverCard driver={driver}/>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    );
}


export default DriversPage;
