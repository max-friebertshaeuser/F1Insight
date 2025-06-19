import { useEffect, useState } from 'react';

export function useDriverStandingsTable(year: number = 2025) {
    const [data, setData] = useState<any[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchStandings() {
            try {
                const response = await fetch('http://localhost:8000/api/catalog/insigth/getdriverstandings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({ year }),
                });

                if (!response.ok) throw new Error('Failed to fetch driver standings');
                const result = await response.json();
                console.log('Fetched driver standings:', result);
                setData(result);
            } catch (err) {
                setError((err as Error).message);
            } finally {
                setLoading(false);
            }
        }

        fetchStandings();
    }, [year]);

    return { data, loading, error };
}
