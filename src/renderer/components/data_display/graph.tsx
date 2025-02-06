import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';



type Chart = { //Think of this like a function declaration like in a header file in c
    title: string,
    xAxis: string,
    yAxis: string
}

export const Chart = ({ title, xAxis, yAxis }: Chart) => <aside>
      <BarChart
        series={[
          { data: [35, 44, 24, 34] },
          { data: [51, 6, 49, 30] },
          { data: [15, 25, 30, 50] },
          { data: [60, 50, 15, 25] },
        ]}
        title={title}
        height={450}
        xAxis={[{ data: ['Q1', 'Q2', 'Q3', 'Q4'], scaleType: 'band' , label: xAxis}]}
        yAxis={[{ label: yAxis}]}
        margin={{ top: 10, bottom: 40, left: 50, right: 10 }}
      />

</aside>
