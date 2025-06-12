import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { ScatterChart } from '@mui/x-charts/ScatterChart';
import { Card, Paper } from '@mui/material';
import { axisClasses } from '@mui/x-charts/ChartsAxis';
import { DatasetType } from '@mui/x-charts/internals';
import { LineChart } from '@mui/x-charts';

import { AxisConfig } from '@mui/x-charts';

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
      xAxis={[{ label: xAxis}]}
      yAxis={[{ label: yAxis, tickMinStep:0.1, tickMaxStep:10}]}
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

export const ChartLineView = ({ title, xAxis, yAxis, data, graphheight, pxheight, legend }: Chart) => {
  return(
  <Card className= "card" variant="outlined" sx={{ height: graphheight+'vh' }}>
    <LineChart 
      dataset={data}
      // @ts-ignore  
      series={[{dataKey: 'y', id: 'placeholder', curve: "linear", baseline: 'min' }]}
      xAxis={[{ dataKey: 'x', label: xAxis}]}
      yAxis={[{ label: yAxis , tickMinStep:0.1, tickMaxStep:2, tickNumber:8}]}
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
  ); 
}



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

export const ChartLineMultiView = ({ title, xAxis, yAxis, graphheight, pxheight, legend, dataset}: ChartMulti) => {

  return(
    <Card className= "card" component= {Paper} variant="outlined" sx={{ height: graphheight+'vh'}}>
      <LineChart 
        dataset={dataset}
        series={[
          {dataKey: 'xx', id: 'xx', curve: "linear" },
          {dataKey: 'xy', id: 'xy', curve: "linear" },
          {dataKey: 'xz', id: 'xz', curve: "linear" },
        ]}
        xAxis={[{ dataKey: 'x', label: xAxis}]}
        yAxis={[{ label: yAxis, tickMinStep: 0.5, tickInterval: Array.from(Array(5000).keys())}]}
        margin={{ top: 10, bottom: 50, left: 50, right: 10 }} 

        // https://stackoverflow.com/questions/77853618/in-mui-x-charts-how-to-prevent-linechart-y-axis-label-from-overlapping-with-tic
        sx={{
          [`.${axisClasses.left} .${axisClasses.label}`]: {
              transform: 'translate(-22px, 0)', // translate the label according to the need
          },
          padding:'14px'
        }}
      />
    </Card> 

  )
  
}

export const ChartMultiView = ({ title, xAxis, yAxis, graphheight, pxheight, legend, dataset}: ChartMulti) => <aside>

  <Card className= "card" component= {Paper} variant="outlined" sx={{ height: graphheight+'vh'}}>
    <ScatterChart 
      dataset={dataset}
      series={[ 
        { datasetKeys: { id: 'id', x: 'x', y: 'xx' }, label: 'X Axis' },
        { datasetKeys: { id: 'id', x: 'x', y: 'xy' }, label: 'Y Axis' },
        { datasetKeys: { id: 'id', x: 'x', y: 'xz' }, label: 'Z Axis' },
      ]}
      xAxis={[{ label: xAxis}]}
      yAxis={[{ label: yAxis}]}
      margin={{ top: 10, bottom: 50, left: 50, right: 10 }} 

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

