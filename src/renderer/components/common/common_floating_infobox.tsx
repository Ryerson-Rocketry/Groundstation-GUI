import { Button, ButtonGroup, Card, Chip, Divider, Grid2, TextField } from '@mui/material';
import '../../css/GeneralStyles.css';
import '../../css/App.css';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import axios from 'axios';
import { useStartingParametersStore, useStatusStore, Coordinate, useGeneralParametersStore } from '../../GlobalStateStores';

/*
function saveStartingCoordinate(coordinate: Coordinate) {
    console.log("set starting coordinates as: "  + useStartingParametersStore((state) => state.mapStartingMarkerCoordinates).x + " " + useStartingParametersStore((state) => state.mapStartingMarkerCoordinates).y);
    useStartingParametersStore((state) => state.setStartingMarkerCoordinates(coordinate));
    console.log("set starting coordinates as: ");
}
*/


//https://iq.js.org/questions/react/how-to-update-a-component-every-second
function TestWrapper() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <div>{time.toLocaleTimeString()}</div>;
}

//Radio
async function CheckFlaskConnection() {
  axios.get('http://127.0.0.1:5000/start')
  .then(function (response) {
    console.log("Radio started: ", response.data);
    useStatusStore.getState().setRadioStatus(true);
  })
  .catch(function (error) {
    console.log(error);
  });
}

const renderGUIRenderStatusComponent = (connectionStatus: boolean) => {
  if (connectionStatus) {
   return <Card className= "card_right_align" variant="outlined" sx={{ background: 'linear-gradient(to right bottom,rgb(3, 3, 3),rgb(113, 255, 156))' }}> Running </Card>
  } else {
   return <Card className= "card_right_align" variant="outlined" sx={{ background: 'linear-gradient(to right bottom,rgb(3, 3, 3),rgb(248, 66, 66))' }}> Paused </Card>
  }
}

const renderServerStatusComponent = (connectionStatus: boolean) => {
  if (connectionStatus) {
   return <Card className= "card_right_align" variant="outlined" sx={{ background: 'linear-gradient(to right bottom,rgb(3, 3, 3),rgb(113, 255, 156))' }}> Connected </Card>
  } else {
   return <Card className= "card_right_align" variant="outlined" sx={{ background: 'linear-gradient(to right bottom,rgb(3, 3, 3),rgb(255, 0, 0))' }}> Error </Card>
  }
}



export const CommonFloatingInfoBox = () => {
    const guiState = useGeneralParametersStore((state) => state.renderGUI);
    const flaskState = useStatusStore((state) => state.flaskStatus);
    const updateFlaskState = useStatusStore((state) => state.setFlaskStatus);
    const radioState = useStatusStore((state) => state.radioStatus);
    const updateRadioState = useStatusStore((state) => state.setRadioStatus);
    
    function ConnectionChecker() {
            
        useEffect(() => {
            const interval = setInterval(async () => {  

                await axios.get('http://127.0.0.1:5000/serverstatus')
                .then(function (response) {
                    //setNewValueArray(response.data); //note since we already parsed the data in python into the proper format, no work to be done here
                    
                    updateFlaskState(response.data[0]["state"]);
                    updateRadioState(response.data[0]["radio_state"]);
                
                })
                .catch(function (error) { //we can assume entire flask server is down thus radio, and flask set to false
                    console.log(error);
                    updateFlaskState(false);
                    updateRadioState(false);
                });
                

            }, 1000);

            return () => clearInterval(interval);
        }, []); 

        return <div></div>

    }

    return (<div className='floating_infobox'>
        {ConnectionChecker()}
        <Card className= "card" variant="outlined" sx={{width: "15vw"}} >   

        <div className='element_row'> Time: <Card className= "card_right_align" variant="outlined"> {TestWrapper()}</Card> </div>
        <div className='element_row'> GUI Status:  {renderGUIRenderStatusComponent(guiState)} </div>
        <div className='element_row'> Flask Status:  {renderServerStatusComponent(flaskState)}</div>
        <div className='element_row'> Radio Status:  {renderServerStatusComponent(radioState)} </div>
             
 



        </Card>
    </div>);



}