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
import geoTempData from "../../../../assets/ne_10m_ocean.json";
import compSatImage from "../../../../assets/testmap.jpg";

import { Card } from '@mui/material';
import { Coordinate, useStartingParametersStore } from '../../GlobalStateStores';


import Map, { Layer, Source } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import axios from 'axios';






/*
//https://maplibre.org/maplibre-gl-js/docs/examples/local-geojson/npm install maplibre-gl
export const GPSMap = ({ initialCoordinatex, initialCoordinatey, initialLaunchPointCoordinate}: GPSMapProps)  => {
  const launchCoords = useStartingParametersStore((state) => state.mapStartingMarkerCoordinates); // proper hook usage (will update)
  const [rocketCoords, setRocketCoords] = React.useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates)); //won't update after this initial set (except if entire component is removed then readded)


  
  return (<Card className= "card" variant="outlined" sx={{ height: '53.2vh' }}>
     <Map
      initialViewState={{
        longitude: -122.4,
        latitude: 37.8,
        zoom: 14
      }}
      style={{width: '44.5vw', height: '53.2vh'}}
      mapStyle={'https://demotiles.maplibre.org/style.json'}
    >
      <Source
        id="oregonjson"
        type="geojson"
        data={geoTempData}
      />


    </Map>

    

  </Card>)



  


}
*/

/*

type GPSMapProps = { //constructor variables
  initialCoordinatex: number,
  initialCoordinatey: number
  initialLaunchPointCoordinate: Coordinate,
  panEnable: boolean
};

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

  var tempZoom = 3000;
  var tempPan = launchCoords;

  React.useEffect(() => {
    const interval = setInterval(async() => {  

      await axios.get('http://127.0.0.1:5000/read/gps/latest')
      .then(function (response) {
          //console.log("recieving data in PageGraph.tsx ");
          setRocketCoords({'x': response.data[0]['x'], 'y': response.data[0]['y']});
      })
      .catch(function (error) {
          console.log(error);
      });


    }, 1000);

    return () => clearInterval(interval);
  }, [panEnable]);   
  

  if (panEnable == true){
    console.log("centered on rocket");
    return (<Card className= "card" variant="outlined" sx={{ height: '53.2vh' }}>
      <ComposableMap projection="geoMercator">
        <ZoomableGroup center={[tempPan.y, tempPan.x]} zoom={tempZoom} minZoom={1} maxZoom={6000} r={0.1}
        onMove={({ x, y, zoom, dragging }) => {
          if (panEnable == true){
            tempPan = {x: y, y: x};
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
            <circle r={0.001} fill="#FF5533" 
            />
            <text
              textAnchor="middle"
              y={0.005}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.005"}}>
                Rocket
            </text>
          </Marker>

            <Marker coordinates={[launchCoords.y, launchCoords.x]}>
            <circle r={0.001} fill="#FF5533"></circle>
            <text
              textAnchor="middle"
              y={0.005}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.005"}}>
                Launch Point
            </text>
    

          </Marker>
        </ZoomableGroup>
      </ComposableMap>
    </Card>)

  }
  else{
        return (<Card className= "card" variant="outlined" sx={{ height: '53.2vh' }}>
      <ComposableMap projection="geoMercator">
        <ZoomableGroup center={[rocketCoords.y, rocketCoords.x]} zoom={tempZoom} minZoom={1} maxZoom={6000} r={0.1}
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
            <circle r={0.001} fill="#FF5533" 
            />
            <text
              textAnchor="middle"
              y={0.005}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.005"}}>
                Rocket
            </text>
          </Marker>

            <Marker coordinates={[launchCoords.y, launchCoords.x]}>
            <circle r={0.001} fill="#FF5533"></circle>
            <text
              textAnchor="middle"
              y={0.005}
              style={{ fontFamily: "system-ui", fill: "#000", fontSize: "0.005"}}>
                Launch Point
            </text>
    

          </Marker>
        </ZoomableGroup>
      </ComposableMap>
    </Card>)
  }
  




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