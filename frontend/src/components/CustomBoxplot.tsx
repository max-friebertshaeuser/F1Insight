import {Group} from '@visx/group';
import {BoxPlot} from '@visx/stats';
import {scaleBand, scaleLinear} from '@visx/scale';
import {useDriverBoxplots} from '../hooks/useDriverBoxplots';
import {Tooltip, useTooltip} from '@visx/tooltip';

type CustomBoxplotProps = {
    driverId: string;
    driverId2?: string;
    width: number;
    height: number;
    team: string;
    team2?: string;
    driverName?: string;
    driverName2?: string;
};
// function jitteredPositions(values: number[]): number[] {
//     return values.map(v => v + Math.random() * 0.3 - 0.15);
// }

export default function CustomBoxplot({driverId, width, height, team, team2, driverId2, driverName2, driverName}: CustomBoxplotProps) {
    const {data: data1, loading: loading1} = useDriverBoxplots(driverId);
    const { data: data2 = [], loading: loading2 }: { data: typeof data1; loading: boolean } = driverId2
        ? useDriverBoxplots(driverId2)
        : { data: [], loading: false } ;

    const teamColor = getComputedStyle(document.documentElement).getPropertyValue(`--color-team-${team}`).trim();
    const teamColor2 = getComputedStyle(document.documentElement).getPropertyValue(`--color-team-${team2}`).trim();

    const {
        tooltipData,
        tooltipLeft,
        tooltipTop,
        tooltipOpen,
        showTooltip,
        hideTooltip,
    } = useTooltip<{
  season: string;
        driver: { name: string; min: number; max: number; median: number };
        driver2?: { name: string; min: number; max: number; median: number };
    }>();


    if (loading1 || !data1 || loading2 || !data2) return <div>Loading...</div>;

    const allData = data1.concat(data2);
    const xDomain = allData.map(d => d.x.toString());
    const xScale = scaleBand({ range: [0, width], domain: xDomain, padding: 0.4 });
    const yMaxVal = Math.max(...allData.flatMap(d => [d.min, d.max]));
    const yMinVal = Math.min(...allData.flatMap(d => [d.min, d.max]));
    const yScale = scaleLinear({ domain: [yMinVal, yMaxVal], range: [height - 60, 0] });
    const boxWidth = xScale.bandwidth();
    const constrained = Math.min(40, boxWidth);


    // @ts-ignore
    return (
        <div className="relative pb-56">
            <svg width={width} height={height}>
                <Group top={40}>
                    {data1.map((d, i) => {
                        const baseX = xScale(d.x.toString())!;

                        return (
                            <g key={`a${i}`}>

                                <BoxPlot
                                    min={d.min}
                                    max={d.max}
                                    left={(xScale(d.x.toString()) ?? 0) - constrained * 0.6}
                                    firstQuartile={d.firstQuartile}
                                    thirdQuartile={d.thirdQuartile}
                                    median={d.median}
                                    boxWidth={constrained}
                                    valueScale={yScale}
                                    fill={teamColor}
                                    stroke="#fff"
                                    strokeWidth={2}
                                    outliers={d.positions.filter(p => p < d.firstQuartile || p > d.thirdQuartile)}

                                    boxProps={{
                                        onMouseEnter: () => {
                                            const driver2SeasonData = data2.find(x => x.x === d.x);

                                            showTooltip({
                                                tooltipLeft: baseX + constrained / 2 ,
                                                tooltipTop: yScale(d.median) ,
                                                tooltipData: {
                                                    season: d.x.toString(),
                                                    driver: {
                                                        name: driverName!,
                                                        median: d.median,
                                                        min: d.min,
                                                        max: d.max,
                                                    },
                                                    driver2: driver2SeasonData
                                                        ? {
                                                            name: driverName2!,
                                                            median: driver2SeasonData.median,
                                                            min: driver2SeasonData.min,
                                                            max: driver2SeasonData.max,
                                                        }
                                                        : undefined,
                                                },
                                            });
                                        },
                                        onMouseLeave: hideTooltip,
                                    }}
                                />
                            </g>
                        );
                    })}

                    {driverId2  && data2.map((d, i) => {
                        const baseX = xScale(d.x.toString())!;
                        return (
                            <g key={`a${i}`}>

                                <BoxPlot
                                    min={d.min}
                                    max={d.max}
                                    left={(xScale(d.x.toString()) ?? 0) + constrained * 0.6}
                                    firstQuartile={d.firstQuartile}
                                    thirdQuartile={d.thirdQuartile}
                                    median={d.median}
                                    boxWidth={constrained}
                                    valueScale={yScale}
                                    fill={teamColor2}
                                    stroke="#fff"
                                    strokeWidth={2}
                                    outliers={d.positions.filter(p => p < d.firstQuartile || p > d.thirdQuartile)}

                                    boxProps={{
                                        onMouseEnter: () => {
                                            const driver2SeasonData = data2.find(x => x.x === d.x);

                                            showTooltip({
                                                tooltipLeft: baseX + constrained / 2 ,
                                                tooltipTop: yScale(d.median) ,
                                                tooltipData: {
                                                    season: d.x.toString(),
                                                    driver: {
                                                        name: driverName!,
                                                        median: d.median,
                                                        min: d.min,
                                                        max: d.max,
                                                    },
                                                    driver2: driver2SeasonData
                                                        ? {
                                                            name: driverName2!,
                                                            median: driver2SeasonData.median,
                                                            min: driver2SeasonData.min,
                                                            max: driver2SeasonData.max,
                                                        }
                                                        : undefined,
                                                },
                                            });
                                        },
                                        onMouseLeave: hideTooltip,
                                    }}
                                />
                            </g>
                        );
                    })}
                </Group>
            </svg>
            {tooltipOpen && tooltipData && (
                <Tooltip
                    top={tooltipTop}
                    left={tooltipLeft}
                    style={{
                        backgroundColor: '#15151E',
                        color: 'white',
                        padding: '6px 10px',
                        borderRadius: '4px',
                        fontSize: '13px',
                        lineHeight: '1.4',
                    }}
                >
                    <div>
                        <strong>{tooltipData.season}</strong></div>
                    <div style={{ display: 'flex', gap: '16px' }}>

                    <div>
                        <strong>{tooltipData.driver.name}:</strong><br />
                        Top Finish: {tooltipData.driver.min}<br />
                        Median: {tooltipData.driver.median}<br />
                        Min Finish: {tooltipData.driver.max}
                    </div>
                    {tooltipData.driver2 && (
                        <div className="">
                            <strong>{tooltipData.driver2.name}:</strong><br />
                            Top Finish: {tooltipData.driver2.min}<br />
                            Median: {tooltipData.driver2.median}<br />
                            Min Finish: {tooltipData.driver2.max}
                        </div>
                    )}
                    </div>
                </Tooltip>
            )}


        </div>
    );
}