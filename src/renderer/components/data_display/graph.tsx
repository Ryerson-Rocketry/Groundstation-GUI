import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { Card } from '@mui/material';

type Chart = {
    title: string,
    xAxis: string,
    yAxis: string
}

export const Chart = ({ title, xAxis, yAxis }: Chart) => <aside>
  <Card className= "card" variant="outlined" sx={{ height: '53.3vh' }}>
    <BarChart 
      series={[
        { data: [35, 44, 24, 34] },
        { data: [51, 6, 49, 30] },
        { data: [15, 25, 30, 50] },
        { data: [60, 50, 15, 25] },
      ]}
      title={title}
      height={500}
      xAxis={[{ data: ['Q1', 'Q2', 'Q3', 'Q4'], scaleType: 'band' , label: xAxis}]}
      yAxis={[{ label: yAxis}]}
      margin={{ top: 10, bottom: 40, left: 50, right: 10 }} 
    />
  </Card>

</aside>
