import { useState, useEffect } from 'react';

export interface DriverBoxplot {
    x: number;
    min: number;
    firstQuartile: number;
    median: number;
    thirdQuartile: number;
    max: number;
    positions: number[];
}

export function useDriverBoxplots(driverId: string) {
    const [data, setData] = useState<DriverBoxplot[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>();

    useEffect(() => {
        let ignore = false;
        async function fetchData() {
            setLoading(true);
            try {
                const res = await fetch('http://localhost:8000/api/catalog/driver/getboxplot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', accept: 'application/json' },
                    body: JSON.stringify({ driver_id: driverId }),
                });
                const json = await res.json();
                if (!ignore) setData(json.boxPlots);
            } catch (e: any) {
                if (!ignore) setError(e.message);
            } finally {
                if (!ignore) setLoading(false);
            }
        }
        fetchData();
        return () => { ignore = true; };
    }, [driverId]);

    console.log('useDriverBoxplots data:', data, 'loading:', loading, 'error:', error);

    return { data, loading, error };
}