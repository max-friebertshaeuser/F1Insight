import {Group} from '@visx/group';
import {BoxPlot} from '@visx/stats';
import {scaleBand, scaleLinear} from '@visx/scale';
import {useDriverBoxplots} from '../hooks/useDriverBoxplots';

type CustomBoxplotProps = {
    driverId: string;
    width: number;
    height: number;
    team: string;
};
// function jitteredPositions(values: number[]): number[] {
//     return values.map(v => v + Math.random() * 0.3 - 0.15);
// }

export default function CustomBoxplot({ driverId, width, height, team }: CustomBoxplotProps) {
    const { data, loading } = useDriverBoxplots(driverId);
    const teamColor = getComputedStyle(document.documentElement).getPropertyValue(`--color-team-${team}`).trim();

    if (loading || !data) return <div>Loading...</div>;

    const xMax = width;
    const yMax = height - 60;

    const xScale = scaleBand({
        range: [0, xMax],
        round: true,
        domain: data.map(d => d.x.toString()),
        padding: 0.4,
    });

    const allValues = data.flatMap(d => [d.min, d.max]);
    const yScale = scaleLinear({
        range: [yMax, 0],
        round: true,
        domain: [Math.min(...allValues), Math.max(...allValues)],
    });

    const boxWidth = xScale.bandwidth();
    const constrainedWidth = Math.min(40, boxWidth);

    return (
        <div className="relative">
            <svg width={width} height={height}>
                <Group top={40}>
                    {data.map((d, i) => (
                        <g key={i}>
                            {/*<ViolinPlot*/}
                            {/*    data={jitteredPositions(d.positions).map(v => ({ value: v }))}*/}
                            {/*    left={xScale(d.x.toString())!}*/}
                            {/*    width={constrainedWidth}*/}
                            {/*    valueScale={yScale}*/}
                            {/*    fill={teamColor}*/}
                            {/*    stroke="#ccc"*/}
                            {/*/>*/}

                            <BoxPlot
                                min={d.min}
                                max={d.max}
                                left={xScale(d.x.toString())!}
                                firstQuartile={d.firstQuartile}
                                thirdQuartile={d.thirdQuartile}
                                median={d.median}
                                boxWidth={constrainedWidth}
                                valueScale={yScale}
                                fill={teamColor}
                                stroke="#fff"
                                strokeWidth={2}
                                outliers={d.positions.filter(p => p < d.firstQuartile || p > d.thirdQuartile)}
                            />
                        </g>
                    ))}
                </Group>
            </svg>
        </div>
    );
}