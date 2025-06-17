import {Group} from '@visx/group';
import {LinePath} from '@visx/shape';
import {scaleLinear} from '@visx/scale';
import {curveBasis, curveMonotoneX} from '@visx/curve';
import {useDriverStandings} from '../hooks/useDriverStandings.ts';
import {useEffect, useState} from "react";

const defaultMargin = { top: 10, right: 10, bottom: 10, left: 10 };

// colors
export const primaryColor = '#8921e0';
export const secondaryColor = '#15151E';
export type GlyphProps = {
    width: number;
    height: number;
    margin?: typeof defaultMargin;
    driverId: string;
    team: string; // e.g., "mclaren", "ferrari"
};

function getCssVar(varName: string) {
    return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
}


export default function CustomGraph({ width, height, margin = defaultMargin, driverId, team }: GlyphProps) {

    const [teamColor, setTeamColor] = useState<string>('');
    const [teamColorShaded, setTeamColorShaded] = useState<string>('');

    useEffect(() => {
        const base = getCssVar(`--color-team-${team}`);
        setTeamColor(base);
        setTeamColorShaded(`color-mix(in srgb, ${base} 60%, black)`);
    }, [team]);



    const backgroundColor = `#15151E`;

    const season =2024; // or pass as prop
    const { data: races, loading, error } = useDriverStandings(driverId, season);

    if (loading || width < 10) return <div>Loading…</div>;
    if (error) return <div>Error: {error}</div>;

    const resultData = races.map((r) => ({
        date: r.round, // just a number now
        value: r.result,
    }));


    const gridData = races.map((r) => ({
        date: r.round,
        value: r.grid,
    }));

    const roundNumbers = races.map((r) => r.round);
    const minRound = Math.min(...roundNumbers);
    const maxRound = Math.max(...roundNumbers);


    const xDomainMin = minRound - 0.5;
    const xDomainMax = maxRound + 0.5;

    const xScale = scaleLinear({
        domain: [xDomainMin, xDomainMax],
        range: [0, width - margin.left - margin.right],
    });




    const allValues = [...resultData, ...gridData].map(d => d.value);
    const maxY = Math.max(...allValues);
    const yScale = scaleLinear({
        domain: [maxY + 1, -1], // give padding top and bottom
        range: [height - margin.top - margin.bottom, 0],
    });


    return (
        <svg width={width} height={height}>
            <rect x={0} y={0} width={width} height={height} fill={backgroundColor} rx={14} />
            <Group left={margin.left} top={margin.top}>
                <LinePath
                    data={resultData}
                    x={(d) => xScale(d.date)}
                    y={(d) => yScale(d.value)}
                    stroke={teamColor}
                    strokeWidth={2}
                    curve={curveMonotoneX}
                />

                <LinePath
                    data={gridData}
                    x={(d) => xScale(d.date)}
                    y={(d) => yScale(d.value)}
                    stroke={teamColorShaded}
                    strokeWidth={2}
                    strokeDasharray="4,4"
                    curve={curveBasis}
                />

                {resultData.map((d, i) => {
                    const left = xScale(d.date);
                    const top = yScale(d.value);
                    return (
                        <g key={i} transform={`translate(${left}, ${top})`}>
                            <circle r={14} fill={backgroundColor} stroke={teamColor} strokeWidth={2} />
                            <text
                                fontSize={12}
                                fontWeight="bold"
                                textAnchor="middle"
                                dy="0.35em"
                                fill={teamColor}
                            >
                                {d.value}
                            </text>
                        </g>
                    );
                })}

            </Group>
        </svg>
    );
}
