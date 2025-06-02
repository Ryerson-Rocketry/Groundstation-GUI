import { Button, ButtonGroup, Card, Chip, Divider, Grid2, TextField } from '@mui/material';
import '../../css/GeneralStyles.css';
import '../../css/App.css';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

import axios from 'axios';
import { useStartingParametersStore, useStatusStore, Coordinate } from '../../GlobalStateStores';



/*
function saveStartingCoordinate(coordinate: Coordinate) {
    console.log("set starting coordinates as: "  + useStartingParametersStore((state) => state.mapStartingMarkerCoordinates).x + " " + useStartingParametersStore((state) => state.mapStartingMarkerCoordinates).y);
    useStartingParametersStore((state) => state.setStartingMarkerCoordinates(coordinate));
    console.log("set starting coordinates as: ");
}
*/
const renderConnectionStatusComponent = (connectionStatus: boolean) => {
  if (connectionStatus) {
   return <div> Running </div>
  } else {
   return <div> No Connection </div>
  }
}

export const StartScreenFloatingToolbox = () => {
    const[tempStartingCoordinate, setTempCoord] = useState(useStartingParametersStore((state) => state.mapStartingMarkerCoordinates));
    const[tempPortID, setPort] = useState(useStartingParametersStore((state) => state.portID));

    function saveStartingCoordinate() {
        useStartingParametersStore.getState().setStartingMarkerCoordinates(tempStartingCoordinate);
        console.log("set starting coordinates as: "  + useStartingParametersStore.getState().mapStartingMarkerCoordinates.x + " " + useStartingParametersStore.getState().mapStartingMarkerCoordinates.y);
    }

    async function savePortID() {
        useStartingParametersStore.getState().setPortID(tempPortID);
        console.log("set port id");
        await axios.get('http://127.0.0.1:5000/radio/port/' + tempPortID)
        .then(function (response) {
            console.log("posted new port id");
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    //{console.log(useStatusStore((state) => state.radioStatus));}
    return ( <div className='floating_toolbox'>
        <Card className= "card" variant="outlined" >   
            <div className='page_content'>
                

                {/*
                <Chip label="Statuses" size="small" />
                
                <div className='element_row'> Radio Run Status: <Card className= "card" variant="outlined"> 
                    {renderConnectionStatusComponent(useStatusStore((state) => state.radioStatus))}
                </Card><br/> </div>
                <div className='element_row'> Flask Connection Status: <Card className= "card" variant="outlined"> 
                    {renderConnectionStatusComponent(useStatusStore((state) => state.flaskStatus))}
                </Card><br/> </div>
                */}
                
            

                <Divider> <Chip label="Starting Parameter" size="small" /> </Divider>
                <TextField id="filled-basic" label="Map Start Coordinates" variant="filled" placeholder={"lat long"} helperText={"Use GCS (Lat Long); Current set is: lat:" + useStartingParametersStore.getState().mapStartingMarkerCoordinates.x + " long:" + useStartingParametersStore.getState().mapStartingMarkerCoordinates.y}
                onChange= {(event) => {setTempCoord({x: parseFloat(event.target.value.split(" ")[0]), y:parseFloat(event.target.value.split(" ")[1])});
                //console.log("saved new coordinates as: " + tempStartingCoordinate.x + " " + tempStartingCoordinate.y)
                }}/>
                <Button onClick={() => {saveStartingCoordinate()}}> <li> Set Starting Coordinates </li> </Button>

                <TextField id="filled-basic" label="Set Radio Serial Port" variant="filled" placeholder={"number"} helperText={"Set Radio Serial Port ID (Default COM5); Current:" + useStartingParametersStore.getState().portID}
                onChange= {(event) => {setPort(parseInt(event.target.value));
                //console.log("saved new coordinates as: " + tempStartingCoordinate.x + " " + tempStartingCoordinate.y)
                }}/>
                <Button onClick={() => {savePortID()}}> <li> Set Port ID </li> </Button>

            </div>    

        </Card>
     </div> );



}