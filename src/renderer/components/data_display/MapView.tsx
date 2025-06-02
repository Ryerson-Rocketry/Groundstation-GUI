import * as React from 'react';
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
import { Coordinate, useStartingParametersStore } from '../../GlobalStateStores';






/*
export const GPSMap = ({ initialCoordinatex, initialCoordinatey, initialLaunchPointCoordinate}: GPSMapProps)  => {
  const launchCoords = useStartingParametersStore((state) => state.mapStartingMarkerCoordinates); // proper hook usage (will update)
  const [rocketCoords, setRocketCoords] = React.useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates)); //won't update after this initial set (except if entire component is removed then readded)

  return (<Card className= "card" variant="outlined" sx={{ height: '53.2vh' }}>
    <ComposableMap projection="geoMercator">
      <ZoomableGroup center={[rocketCoords.y, rocketCoords.x]} zoom={100} minZoom={1} maxZoom={500} r={0.1}>
        <Geographies geography={geoData}>
          {({ geographies}) =>
            geographies.map((geo) => (
              <Geography key={geo.rsmKey} 
              geography={geo}
              fill="#DDD"
              stroke='#000'
              strokeWidth={0.01}
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
        
        <Marker coordinates={[initialCoordinatex, initialCoordinatey]} >
          <circle r={0.05} fill="#FF5533" 
          />
          <text
            textAnchor="middle"
            y={0.4}
            style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.2"}}>
              Rocket
          </text>
        </Marker>

          <Marker coordinates={[initialLaunchPointCoordinate.x, initialLaunchPointCoordinate.y]}>
          <circle r={0.05} fill="#FF5533"></circle>
          <text
            textAnchor="middle"
            y={0.4}
            style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.2"}}>
              Launch Point
          </text>
  

        </Marker>
      </ZoomableGroup>
    </ComposableMap>
  </Card>)


  


}
*/

type GPSMapProps = { //constructor variables
  initialCoordinatex: number,
  initialCoordinatey: number
  initialLaunchPointCoordinate: Coordinate,
  panEnable: boolean
};

export const GPSMap = ({ initialCoordinatex, initialCoordinatey, initialLaunchPointCoordinate, panEnable}: GPSMapProps) => {
  const launchCoords = useStartingParametersStore((state) => state.mapStartingMarkerCoordinates); // proper hook usage (will update)
  const [rocketCoords, setRocketCoords] = React.useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates)); //won't update after this initial set (except if entire component is removed then readded)
  

  const [zoomLevel, setZoom] = React.useState(1);

  const [panCoords, setPan] = React.useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates));

  var tempZoom = 1000;
  var tempPan = {x: 31.0498056, y: -103.39730555555556};

  React.useEffect(() => {
    const interval = setInterval(() => {  

      var coords: Coordinate;
      coords = {x: 31.0498056 + Math.random() * (0.1), y: -103.39730555555556};

      setRocketCoords(coords);

      if (panEnable == true){
        tempPan = coords;
      }



    }, 1000);

    return () => clearInterval(interval);
  }, [panEnable]);   
  
 
  return (<Card className= "card" variant="outlined" sx={{ height: '53.2vh' }}>
    <ComposableMap projection="geoMercator">
      <ZoomableGroup center={[tempPan.y, tempPan.x]} zoom={tempZoom} minZoom={1} maxZoom={1500} r={0.1}
      onMove={({ x, y, zoom, dragging }) => {
        if (panEnable == true){
          console.log("pan");
          tempPan = rocketCoords;
        }
        else{
          tempPan = {x : y, y : x};
          tempZoom = zoom;
        }

        //tempZoom = zoom;
        //tempPan = {x: y, y: x};
      }}
      >
        <Geographies geography={geoData}>
          {({ geographies}) =>
            geographies.map((geo) => (
              <Geography key={geo.rsmKey} 
              geography={geo}
              fill="#DDD"
              stroke='#000'
              strokeWidth={0.01}
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
        
        <Marker coordinates={[rocketCoords.y, rocketCoords.x]} >
          <circle r={0.01} fill="#FF5533" 
          />
          <text
            textAnchor="middle"
            y={0.02}
            style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.01"}}>
              Rocket
          </text>
        </Marker>

          <Marker coordinates={[launchCoords.y, launchCoords.x]}>
          <circle r={0.01} fill="#FF5533"></circle>
          <text
            textAnchor="middle"
            y={0.02}
            style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.01"}}>
              Launch Point
          </text>
  

        </Marker>
      </ZoomableGroup>
    </ComposableMap>
  </Card>)





}


/*
type GPSMapState = { //class "instance" variables
  currentCoordinatex: number,
  currentCoordinatey: number,
  launchPointCoordinate: Coordinate
}

export class GPSMap extends React.Component<GPSMapProps, GPSMapState>{
  state: GPSMapState = { //initialize instance variables
    currentCoordinatex: this.props.initialCoordinatex,
    currentCoordinatey: this.props.initialCoordinatey,
    launchPointCoordinate: this.props.initialLaunchPointCoordinate
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
                strokeWidth={0.01}
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
            <circle r={0.05} fill="#FF5533" 
            />
            <text
              textAnchor="middle"
              y={0.4}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.2"}}>
                Rocket
            </text>
          </Marker>

            <Marker coordinates={[this.state.launchPointCoordinate.x, this.state.launchPointCoordinate.y]}>
            <circle r={0.05} fill="#FF5533"></circle>
            <text
              textAnchor="middle"
              y={0.4}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.2"}}>
                Launch Point
            </text>
   

          </Marker>
        </ZoomableGroup>
      </ComposableMap>
    </Card>

    
  }
}
*/