import { useEffect, useState } from 'react';
import TeamCard, {type Team} from '../components/TeamCard.tsx';

const TeamsPage = () => {
    const [teams, setTeams] = useState<Partial<Team>[]>([]);

    useEffect(() => {
        const fetchTeams = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/catalog/getcurrentteams', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({}),
                });

                let data: Partial<Team>[] = (await res.json())['teams'];
                console.log('Fetched teams:', data);
                data = data.sort((a, b) => (a.position ?? 0) - (b.position ?? 0));
                setTeams(data);
            } catch (err) {
                console.error('Failed to fetch teams:', err);
            }
        };

        fetchTeams();
    }, []);


    return (
        <div className="overflow-auto min-h-screen bg-f1-black text-f1-white font-fregular p-4 flex justify-center">
            <div className="w-full max-w-7xl">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-4 sm:px-8">
                    {teams.map((team) => (
                        <div key={team.team_id! + team.position!} className="flex justify-center mb-8">
                            <TeamCard team={team} />
                        </div>
                    ))}
                </div>
            </div>

        </div>
    );
};

export default TeamsPage;
