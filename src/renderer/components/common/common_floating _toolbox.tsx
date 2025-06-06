import { Button, ButtonGroup, Card, Chip, Divider, Grid2, TextField } from '@mui/material';
import '../../css/GeneralStyles.css';
import '../../css/App.css';
import React, { useState } from 'react';
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

export const CommonFloatingToolBox = () => {
    const guiState = useGeneralParametersStore((state) => state.renderGUI);
    const updateGuiState = useGeneralParametersStore((state) => state.setRenderGUI);
    
    return (<div className='floating_toolbox'>
        <Card className= "card" variant="outlined" >   

                <div className='element_row'> Utilities <Card className= "card" variant="outlined"> 
                </Card><br/> </div>
                <ButtonGroup variant="contained" aria-label="Stataus">
                    <Button onClick={() => {updateGuiState(true)}}> <li> Start GUI </li> </Button>
                    <Button onClick={() => {updateGuiState(false)}}> <li> Stop GUI </li> </Button>
                </ButtonGroup>  

        </Card>
    </div>);



}