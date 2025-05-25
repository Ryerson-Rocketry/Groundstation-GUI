import { Button, ButtonGroup, Card, Chip, Divider, Grid2 } from '@mui/material';
import '../../css/GeneralStyles.css';
import React from 'react';
import { Link } from 'react-router-dom';

import axios from 'axios';



export const FloatingToolbox = () => {
    const[guiState, setState] = useState(false);

    useEffect(() => {
        console.log("useEffect runs"); 

        const interval = setInterval(async () => {
            setCount((prevCount) => prevCount + 1);
        }, 1000);

        return () => clearInterval(interval); 
    }, []); 
    
    async getRadio(){
        await axios.get('http://127.0.0.1:5000/radio/status')
                .then(function (response) {
                    console.log("pinging radio for status");
                    return(response.data);
                })
                .catch(function (error) {
                    console.log(error);
                });
        return null;
    }


    return ( <div className='floating_toolbox'>
        <Card className= "card" variant="outlined" >   
            <div className='page_content'>
                Radio Status: <br></br>
                <ButtonGroup variant="contained" aria-label="Stataus">
                    <Button onClick={() => {setRenderState(true);}}> <li> Start GUI </li> </Button>
                    <Button onClick={() => {setRenderState(false);}}> <li> Stop GUI </li> </Button>
                </ButtonGroup>  
            </div>    

        </Card>
     </div> );



}