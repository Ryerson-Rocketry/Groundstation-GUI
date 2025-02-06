import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
  Marker
} from "react-simple-maps";


import {
  blueberryTwilightPalette,
  mangoFusionPalette,
  cheerfulFiestaPalette,
} from '@mui/x-charts/colorPalettes';

import geoData from "../../../../assets/us.json";

type GPSMap = { //Think of this like a function declaration like in a header file in c
    title: string,
    xAxis: string
}



export const GPSMap = ({ title, xAxis }: GPSMap) => <aside>
  <div>
    <ComposableMap projection="geoMercator"  >
      <ZoomableGroup center={[0, 0]} zoom={50}>
        <Geographies geography={geoData}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography key={geo.rsmKey} geography={geo} />
            ))
          }
        </Geographies>
        <Marker coordinates={[0, 0]}>
          <circle r={3} fill="#FF5533" />
        </Marker>
      </ZoomableGroup>
    </ComposableMap>
  </div>
</aside>

