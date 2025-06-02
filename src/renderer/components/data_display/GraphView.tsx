import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { ScatterChart } from '@mui/x-charts/ScatterChart';
import { Card } from '@mui/material';
import { axisClasses } from '@mui/x-charts/ChartsAxis';
import { DatasetType } from '@mui/x-charts/internals';

/*
type Chart = {
    title: string,
    xAxis: string,
    yAxis: string
}


export const ChartView = ({ title, xAxis, yAxis }: Chart) => <aside>
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
*/

export type DataPoint = {
  x: number;
  y: number;
  id: number;
};

type Chart = {
  title: string;
  xAxis: string;
  yAxis: string;
  data: DataPoint[];

  graphheight: number
  pxheight: number

  legend: string;
};

export const ChartView = ({ title, xAxis, yAxis, data, graphheight, pxheight, legend }: Chart) => <aside>



  <Card className= "card" variant="outlined" sx={{ height: graphheight+'vh' }}>
    <ScatterChart 
      series={[{ data, label: legend, id: 'placeholder' }]}
      height={pxheight}
      xAxis={[{ label: xAxis}]}
      yAxis={[{ label: yAxis}]}
      margin={{ top: 10, bottom: 40, left: 50, right: 10 }} 

      // https://stackoverflow.com/questions/77853618/in-mui-x-charts-how-to-prevent-linechart-y-axis-label-from-overlapping-with-tic
      sx={{
        [`.${axisClasses.left} .${axisClasses.label}`]: {
            transform: 'translate(-22px, 0)', // translate the label according to the need
        },
        padding:'14px'
      }}
    />
  </Card> 

</aside>


export type DataPointAccelerometer = {
    x: number;
    xx: number;
    xy: number;
    xz: number;
    id: string;
};

type ChartMulti = {
  title: string;
  xAxis: string;
  yAxis: string;

  graphheight: number
  pxheight: number

  legend: string;

  dataset: DataPointAccelerometer[]
};

export const ChartMultiView = ({ title, xAxis, yAxis, graphheight, pxheight, legend, dataset}: ChartMulti) => <aside>

  <Card className= "card" variant="outlined" sx={{ height: graphheight+'vh' }}>
    <ScatterChart 
      dataset={dataset}
      series={[ 
        { datasetKeys: { id: 'id', x: 'x', y: 'xx' }, label: 'X Axis' },
        { datasetKeys: { id: 'id', x: 'x', y: 'xy' }, label: 'Y Axis' },
        { datasetKeys: { id: 'id', x: 'x', y: 'xz' }, label: 'Z Axis' },
      ]}
      height={pxheight}
      xAxis={[{ label: xAxis}]}
      yAxis={[{ label: yAxis}]}
      margin={{ top: 10, bottom: 40, left: 50, right: 10 }} 

      // https://stackoverflow.com/questions/77853618/in-mui-x-charts-how-to-prevent-linechart-y-axis-label-from-overlapping-with-tic
      sx={{
        [`.${axisClasses.left} .${axisClasses.label}`]: {
            transform: 'translate(-22px, 0)', // translate the label according to the need
        },
        padding:'14px'
      }}
    />
  </Card> 

</aside>

