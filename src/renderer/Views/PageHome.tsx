import React, { useState, useEffect } from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageHome.css';

import Card from '@mui/material/Card';
import { Button, ButtonGroup, Chip, createTheme, Divider, FormControl, FormControlLabel, FormLabel, Grid2, Radio, RadioGroup, ThemeProvider, useColorScheme } from '@mui/material';

import {ChartView, DataPoint} from '../components/data_display/GraphView';
import {GPSMap} from '../components/data_display/MapView';

import { NavHeader } from '../components/common/nav_header';
import { FloatingToolbox } from '../components/common/floating_toolbox';

import GaugeComponent from 'react-gauge-component';
import { Link } from 'react-router-dom';

//const ChartComponent  = <ChartView title="Placeholder Vs. Time" xAxis="Time (Sec)" yAxis="PLACEHOLDER (UNITS)" />
//const MapComponent  = <GPSMap initialCoordinatex={-100} initialCoordinatey={40} />;

import axios from 'axios';
import { render } from '@testing-library/react';

//https://iq.js.org/questions/react/how-to-update-a-component-every-second
function TestWrapper() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <p>The current time is: {time.toLocaleTimeString()}</p>;
}









const Layout = () => {
    const [graphIndex, setGraphIndex] = useState(0);
    const [renderState, setRenderState] = useState(false);

    function ChartWrapper(ind : number) {
        const [newData, setNewData] = useState([{x:3, y:4, id: 0}]);

        useEffect(() => {
            const interval = setInterval(async () => {  
                if (renderState == true){
                    await axios.get('http://127.0.0.1:5000/read/graph/' + ind)
                    .then(function (response) {
                        console.log("recieving data in PageHome.tsx using:" + ind);
                        setNewData(response.data); //note since we already parsed the data in python into the proper format, no work to be done here
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                }

            }, 100);

            return () => clearInterval(interval);
        }, [graphIndex, renderState]); //note, [graphIndex] is considered a dependency and thus this interval will be rerendered (with the new graphIndex value) every time graph index changes

    return <ChartView title="Placeholder Vs. Time" xAxis="placehodler" yAxis="PLACEHOLDER (UNITS)" data = { newData } />;
    }

    function MapWrapper() {
        const [newCoordinates, setNewCoordinates] = useState(40);

        useEffect(() => {
            const interval = setInterval(() => {  
                if (renderState == true){
                    setNewCoordinates(40 + Math.random() * (42 - 40));
                    //console.log("reading "+  40 + Math.random() * (42 - 40));
                }

            }, 1000);

            return () => clearInterval(interval);
        }, [graphIndex]); 

        return <GPSMap initialCoordinatex={-100} initialCoordinatey={newCoordinates} />;
    }

    function TextWrapper() {
        const [valueArray, setNewValueArray] = useState([0, 0, 0, 0, 0, 0]);
        const [dictNameMatch] = useState(["Pressure", "Temperature", "Voltage", "X Axis Acceleration","Y Axis Acceleration", "Z Axis Acceleration"])
        const [dictUnitMatch] = useState(["mBar", "C", "V", "G", "G", "G"])
        
        useEffect(() => {
            const interval = setInterval(async () => {  
                if (renderState == true){
                    await axios.get('http://127.0.0.1:5000/read/last/0')
                    .then(function (response) {
                        //console.log(response.data);
                        setNewValueArray(response.data); //note since we already parsed the data in python into the proper format, no work to be done here
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                }

            }, 1000);

            return () => clearInterval(interval);
        }, [valueArray, renderState]); 
        
        

        return (
            
            [...Array(6).keys()].map((key) => (
                <Card className= "card" variant="outlined" key={key}> 
                    {dictNameMatch[key]}
                    <br/>
                    {valueArray[key]}  {dictUnitMatch[key]} 

                </Card>
            ))

        
        
        );
    }

    return (
        <div className='page_container'>

            <div className='floating_toolbox'>
                <Card className= "card" variant="outlined" >   
                    <div className='page_content'>
                        Radio Status: <br></br>
                        <ButtonGroup variant="contained" aria-label="Stataus">
                            <Button onClick={() => {setRenderState(true);}}> <li> Start GUI </li> </Button>
                            <Button onClick={() => {setRenderState(false);}}> <li> Stop GUI </li> </Button>
                        </ButtonGroup>  
                    </div>    

                </Card>
            </div>
            
            <NavHeader/>

            <div className='page_content'>
                <div className='overall_container'>
                    {TestWrapper()}

                    <div className="page_title">Dashboard</div>

                    <div className='center_container'>
                        <div className="map_container">
                            {MapWrapper()}
                        </div>
                        <div className="graph_container">
                            <Card className= "card" variant="outlined" >
                                <FormControl >
                                    <FormLabel id="demo-radio-buttons-group-label">Telemetry Graphs</FormLabel>
                                    <RadioGroup
                                        row
                                        aria-labelledby="demo-radio-buttons-group-label"
                                        defaultValue="1"
                                        name="radio-buttons-group" 
                                    >
                                        <FormControlLabel value="1" control={<Radio />} label="Pressure"  onClick={() => {setGraphIndex(0);}} />
                                        <FormControlLabel value="2" control={<Radio />} label="Temperature" onClick={() => {console.log("changed to temperature graph old index was " + graphIndex); setGraphIndex(2);}} />
                                        <FormControlLabel value="3" control={<Radio />} label="Voltage" onClick={() => {setGraphIndex(3);}} />
                                        <FormControlLabel value="4" control={<Radio />} label="Acceleration" onClick={() => {setGraphIndex(4);}} />
                                    </RadioGroup>
                                </FormControl>
      
                            </Card>
                            
                            {ChartWrapper(graphIndex)} 
                        </div>    
                    </div>

                    <div className='bottom_container'>
                        <Divider component="li"> <Chip label="Raw Data Readout (Current)" size="small" /></Divider>
                        <Card className= "gauge_row" variant="outlined"> 
                            {TextWrapper()}
                        </Card>
                            
                    </div>


                </div>
            </div>

             
            
        </div>
    )
  };
  
  export default Layout;