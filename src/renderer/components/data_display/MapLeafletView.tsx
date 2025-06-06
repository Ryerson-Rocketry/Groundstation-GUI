import * as React from 'react';

import { Card } from '@mui/material';
import { Coordinate, useGeneralParametersStore, useStartingParametersStore } from '../../GlobalStateStores';

import L, {LatLngBoundsExpression, LatLngExpression, Map} from "leaflet";
import "leaflet.offline";

import { MapContainer } from "react-leaflet";
import "leaflet.offline";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from 'react';

import rocketMarker from "../../../../assets/map/normal_marker.png";
import launchMarker from "../../../../assets/map/star_marker.png";
import backupMap from "../../../../assets/launchsitebackup.png";
import axios from 'axios';

var rocketIcon = L.icon({
    iconUrl: rocketMarker,

    iconSize:     [45, 45], // size of the icon
    iconAnchor:   [22, 35], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var launchIcon = L.icon({
    iconUrl: launchMarker,

    iconSize:     [45, 45], // size of the icon
    iconAnchor:   [22, 35], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});


type LeafletMapProps = { //constructor variables
  width: string
  height: string
  freePan: boolean
  showBackupMap : boolean
};

//NOTE: Solutions here are modified from https://stackoverflow.com/questions/69091797/using-leaflet-offline-with-react

export type markerData = {
  marker: L.Marker<any>
};

export const LeafletMap = ({ width, height, freePan, showBackupMap}: LeafletMapProps) => {
  const [map, setMap] = useState<Map | undefined>();
  const renderState = useGeneralParametersStore((state) => state.renderGUI);
  const [launchCoords, setLaunchCoords] = useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates));
  const [rocketCoords, setRocketCoords] = useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates));
  const [onFirstSetup, setFirstSetup] = useState(true);

  const[currentRocketMarker, setCurrentRocketMarker] = useState<L.Marker<any>>(L.marker([launchCoords.x, launchCoords.y], {icon: rocketIcon})); //dummy marker
  
  useEffect(() => {
    const interval = setInterval(async () => {  
      if (renderState == true){
        await axios.get('http://127.0.0.1:5000/read/gps/latest')
        .then(function (response) {
            //console.log("recieving data in PageGraph.tsx ");
            setRocketCoords({'x': response.data[0]['x'], 'y': response.data[0]['y']});
        })
        .catch(function (error) {
            console.log(error);
      });
      }

      
    }, 1000);

    return () => clearInterval(interval);
  }, [map, freePan, renderState]);   

  useEffect(() => {
   
      if (freePan == false){ //assumes rocket is centered
            console.log(freePan);
            if (map != null){
              map.setView(L.latLng(rocketCoords.x,rocketCoords.y),15);
            } 
          }


    return ;
  }, [map, freePan, rocketCoords]);  

  useEffect(() => {
    if(map){
    
      if (onFirstSetup == true){ //only render gui controls on first render
        // @ts-ignore
        const tileLayerOffline = L.tileLayer.offline(
          "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            minZoom: 13,
          }
        );

        tileLayerOffline.addTo(map);
        
        // @ts-ignore
        const controlSaveTiles = L.control.savetiles(
          tileLayerOffline, 
          {
            zoomlevels: [1], // optional zoomlevels to save, default current zoomlevel
          }
        );

        
        controlSaveTiles.addTo(map!);

        L.marker([launchCoords.x, launchCoords.y], {icon: launchIcon}).addTo(map).bindPopup("Launch Point");

        if (showBackupMap == true){
          //var backupMap = L.marker([launchCoords.x, launchCoords.y], {icon: backupMapIcon}).addTo(map);
          var imageBounds: LatLngBoundsExpression;
          const scale = 0.120;
          imageBounds = [[launchCoords.x -scale, launchCoords.y -scale], [launchCoords.x + scale, launchCoords.y + scale]];

          L.imageOverlay(backupMap, imageBounds).addTo(map);
        }
        
        setFirstSetup(false);
      }
    
    //delete previous markers from previous rerender
    map.removeLayer(currentRocketMarker);

    var markerR = L.marker([rocketCoords.x, rocketCoords.y], {icon: rocketIcon}).addTo(map); //create the latest marker from rerender
    markerR.setZIndexOffset(50);

    markerR.bindTooltip("Rocket");

    //add marker to marker tracking list
    setCurrentRocketMarker(markerR);
  }

}, [map, rocketCoords, launchCoords, showBackupMap]);

  return(
    <MapContainer
      style={{ width: width, height: height }}
      center={[rocketCoords.x, rocketCoords.y]}
      zoom={1}
      scrollWheelZoom={true}
      // @ts-ignore
      ref={setMap}
    >
    </MapContainer>
  )
}


