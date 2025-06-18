import {Group} from '@visx/group';
import {LinePath} from '@visx/shape';
import {scaleLinear} from '@visx/scale';
import {curveBasis, curveMonotoneX} from '@visx/curve';
import {useDriverStandings} from '../hooks/useDriverStandings.ts';
import {useEffect, useState} from "react";
import {useTooltip, Tooltip} from '@visx/tooltip';

const defaultMargin = {top: 10, right: 10, bottom: 10, left: 10};

// colors

export type GlyphProps = {
    width: number;
    height: number;
    margin?: typeof defaultMargin;
    driverId: string;
    driverId2?: string; // Optional second driver
    team: string;
    season: number;
    team2?: string; // Optional second team, not used yet
    driverName?: string; // Optional driver name for tooltip
    driverName2?: string; // Optional second driver name for tooltip
};

function getCssVar(varName: string) {
    return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
}


export default function CustomGraph({
                                        width,
                                        height,
                                        margin = defaultMargin,
                                        driverId,
                                        driverId2,
                                        team,
                                        team2,
                                        season,
                                        driverName, driverName2
                                    }: GlyphProps) {

    const [teamColor, setTeamColor] = useState<string>('');
    const [teamColorShaded, setTeamColorShaded] = useState<string>('');
    const [team2Color, setTeam2Color] = useState<string>('');
    const [team2ColorShaded, setTeam2ColorShaded] = useState<string>('');

    const {
        tooltipData,
        tooltipLeft,
        tooltipTop,
        tooltipOpen,
        showTooltip,
        hideTooltip,
    } = useTooltip<{ name: string }>();


    const name1 = driverName;
    const name2 = driverId2 ? driverName2 : undefined;

    useEffect(() => {
        const base = getCssVar(`--color-team-${team}`);
        setTeamColor(base);
        setTeamColorShaded(`color-mix(in srgb, ${base} 60%, black)`);

        if (team2) {
            const base2 = getCssVar(`--color-team-${team2}`);
            // Slight hue shift via mix with another color (blue here is a placeholder for offset)
            const modified = `color-mix(in srgb, ${base2} 80%, black 40%)`;
            const modifiedShaded = `color-mix(in srgb, ${base2} 60%, black 80%)`;

            setTeam2Color(modified);
            setTeam2ColorShaded(modifiedShaded);
        } else {
            setTeam2Color('');
            setTeam2ColorShaded('');
        }
    }, [team, team2]);


    const backgroundColor = `#15151E`;

    const {data: races1, loading: loading1, error: error1} = useDriverStandings(driverId, season);
    const {
        data: races2,
        loading: loading2,
        error: error2
    } = driverId2 ? useDriverStandings(driverId2!, season) : {data: [], loading: false, error: undefined};

    if (loading1 || (driverId2 && loading2) || width < 10) {
        return (
            <div style={{width, height}}
                 className="bg-f1-black rounded-xl flex items-center justify-center text-white/30 font-fwide text-xl">
                Loading graph...
            </div>
        );
    }

    if (error1 || (driverId2 && error2)) return <div>Error loading driver data</div>;


    const resultDataDriver1 = races1.map((r) => ({date: +r.round, value: r.result}));
    const gridDataDriver1 = races1.map((r) => ({date: +r.round, value: r.grid}));

    const resultDataDriver2 = driverId2 ? races2.map((r) => ({date: +r.round, value: r.result})) : [];
    const gridDataDriver2 = driverId2 ? races2.map((r) => ({date: +r.round, value: r.grid})) : [];


    const roundNumbers = [...races1, ...races2].map((r) => +r.round);
    const minRound = Math.min(...roundNumbers);
    const maxRound = Math.max(...roundNumbers);


    const xDomainMin = minRound - 0.5;
    const xDomainMax = maxRound + 0.5;

    const xScale = scaleLinear({
        domain: [xDomainMin, xDomainMax],
        range: [0, width - margin.left - margin.right],
    });


    const allValues = [...resultDataDriver1, ...gridDataDriver1, ...resultDataDriver2, ...gridDataDriver2]
        .map((d) => d.value)
    const maxY = Math.max(...allValues);
    const yScale = scaleLinear({
        domain: [maxY + 1, -1], // give padding top and bottom
        range: [height - margin.top - margin.bottom, 0],
    });


    return (
        <div className="relative">
            {tooltipOpen && tooltipData && (
                <Tooltip top={tooltipTop} left={tooltipLeft}
                         style={{
                             backgroundColor: '#15151E', // black-ish
                             color: 'white',
                             padding: '4px 8px',
                             borderRadius: '4px',
                             boxShadow: '0 0 10px rgba(0,0,0,0.5)',
                             fontFamily: 'sans-serif',
                             fontSize: '14px',
                             position: 'absolute',
                         }}
                >
                    {tooltipData.name}
                </Tooltip>
            )}

            <svg width={width} height={height}>
                <rect x={0} y={0} width={width} height={height} fill={backgroundColor} rx={14}/>
                <Group left={margin.left} top={margin.top}>
                    {/* Driver 1 - real team color */}
                    <LinePath
                        data={resultDataDriver1}
                        x={(d) => xScale(d.date)}
                        y={(d) => yScale(d.value)}
                        stroke={teamColor}
                        strokeWidth={2}
                        curve={curveMonotoneX}
                    />

                    <LinePath
                        data={gridDataDriver1}
                        x={(d) => xScale(d.date)}
                        y={(d) => yScale(d.value)}
                        stroke={teamColorShaded}
                        strokeWidth={2}
                        strokeDasharray="4,4"
                        curve={curveBasis}
                    />

                    {resultDataDriver1.filter((d) => typeof d.value === 'number' && !isNaN(d.value))
                        .map((d, i) => {
                            const left = xScale(d.date);
                            const top = yScale(d.value);
                            console.log(`Driver 1: ${d.value} at (${left}, ${top})`);
                            return (
                                <g key={i} transform={`translate(${left}, ${top})`}>
                                    <circle
                                        r={14}
                                        fill={backgroundColor}
                                        stroke={teamColor}
                                        strokeWidth={2}
                                        onMouseEnter={() =>
                                            showTooltip({
                                                tooltipLeft: xScale(d.date) + margin.left,
                                                tooltipTop: yScale(d.value) + margin.top - 20,
                                                tooltipData: {name: name1!},
                                            })
                                        }
                                        onMouseLeave={hideTooltip}
                                    />
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

                    {driverId2 && (
                        <>
                            {/* Driver 2 - secondary color (temporary) */}
                            <LinePath
                                data={resultDataDriver2}
                                x={(d) => xScale(d.date)}
                                y={(d) => yScale(d.value)}
                                stroke={team2Color}
                                strokeWidth={2}
                                curve={curveMonotoneX}
                            />

                            <LinePath
                                data={gridDataDriver2}
                                x={(d) => xScale(d.date)}
                                y={(d) => yScale(d.value)}
                                stroke={team2ColorShaded}
                                strokeWidth={2}
                                strokeDasharray="4,4"
                                curve={curveBasis}
                            />


                            {resultDataDriver2.filter((d) => typeof d.value === 'number' && !isNaN(d.value))
                                .map((d, i) => {
                                    const left = xScale(d.date);
                                    const top = yScale(d.value);
                                    return (
                                        <g key={i} transform={`translate(${left}, ${top})`}>
                                            <circle
                                                r={14}
                                                fill={backgroundColor}
                                                stroke={team2Color}
                                                strokeWidth={2}
                                                onMouseEnter={() =>
                                                    showTooltip({
                                                        tooltipLeft: xScale(d.date) + margin.left,
                                                        tooltipTop: yScale(d.value) + margin.top - 20,
                                                        tooltipData: {name: name2!},
                                                    })
                                                }
                                                onMouseLeave={hideTooltip}
                                            />
                                            <text
                                                fontSize={12}
                                                fontWeight="bold"
                                                textAnchor="middle"
                                                dy="0.35em"
                                                fill={team2Color}
                                            >
                                                {d.value}
                                            </text>
                                        </g>
                                    );
                                })}
                        </>
                    )}
                </Group>
            </svg>
        </div>
    );
}
