export function getTeamClass(teamName: string): string {
    const map: Record<string, string> = {
        'mercedes': 'mercedes',
        'red bull': 'redbull',
        'ferrari': 'ferrari',
        'mclaren': 'mclaren',
        'aston martin': 'astonmartin',
        'alpine f1 team': 'alpine',
        'williams': 'williams',
        'sauber': 'sauber', // Sauber as Alfa Romeo stand-in
        'haas f1 team': 'haas',
        'rb f1 team': 'racingbull' // assuming RB is Red Bull’s second team
    };

    const key = teamName.trim().toLowerCase();
    return map[key] || 'default';
}
