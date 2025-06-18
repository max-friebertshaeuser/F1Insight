import { useState, useEffect } from 'react';

interface RaceResult {
    round: number;
    grid: number;
    result: number;
}

export function useDriverStandings(driverId: string, season: number) {
    const [data, setData] = useState<RaceResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | undefined>();

    useEffect(() => {
        let ignore = false;
        const fetchStandings = async () => {
            setLoading(true);
            setError(undefined);
            try {
                const res = await fetch('http://localhost:8000/api/catalog/driver/getstandings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', accept: 'application/json' },
                    body: JSON.stringify({ driver_id: driverId, season }),
                });

                if (!ignore) {
                    const json = await res.json();

                    const sorted = json.races
                        .slice()
                        .sort((a: RaceResult, b: RaceResult) => a.round - b.round);

                    setData(sorted);
                }
            } catch (e: any) {
                if (!ignore) setError(e.message);
            } finally {
                if (!ignore) setLoading(false);
            }
        };

        fetchStandings();
        return () => {
            ignore = true;
        };
    }, [driverId, season]);

    return { data, loading, error };
}
