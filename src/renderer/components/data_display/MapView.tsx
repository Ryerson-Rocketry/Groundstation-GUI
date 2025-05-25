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

import geoData from "../../../../assets/counties-10m.json";
import compSatImage from "../../../../assets/testmap.jpg";
import { Card } from '@mui/material';


type GPSMapState = { //class "instance" variables
  currentCoordinatex: number,
  currentCoordinatey: number,
}

type GPSMapProps = { //constructor variables
  initialCoordinatex: number,
  initialCoordinatey: number
};

export class GPSMap extends React.Component<GPSMapProps, GPSMapState>{
  state: GPSMapState = { //initialize instance variables
    currentCoordinatex: this.props.initialCoordinatex,
    currentCoordinatey: this.props.initialCoordinatey
  };

  render() { //frontend component
    return <Card className= "card" variant="outlined" sx={{ height: '60vh' }}>
      <ComposableMap projection="geoMercator">
        <ZoomableGroup center={[this.state.currentCoordinatex, this.state.currentCoordinatey]} zoom={15} minZoom={1} maxZoom={500} r={0.1}>
          <Geographies geography={geoData}>
            {({ geographies}) =>
              geographies.map((geo) => (
                <Geography key={geo.rsmKey} 
                geography={geo}
                fill="#DDD"
                stroke='#000'
                strokeWidth={0.1}
                //https://github.com/zcreativelabs/react-simple-maps/issues/166
                style={{   
                  default: { outline: "none" },
                  hover: { outline: "none" },
                  pressed: { outline: "none" },
                }}
                />
              ))
            }
          </Geographies>
          
          <Marker coordinates={[this.state.currentCoordinatex, this.state.currentCoordinatey]} >
            <circle r={0.25} fill="#FF5533" 
            />
            <text
              textAnchor="middle"
              y={0.4}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.2"}}>
                Rocket
            </text>

            <img src={ compSatImage } />
          </Marker>

            <Marker coordinates={[this.state.currentCoordinatex, this.state.currentCoordinatey]}>
               
   

            </Marker>
        </ZoomableGroup>
      </ComposableMap>
    </Card>

    
  }
}