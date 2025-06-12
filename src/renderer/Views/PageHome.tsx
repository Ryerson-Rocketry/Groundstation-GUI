import React, { useState, useEffect } from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageHome.css';

import Card from '@mui/material/Card';
import { Button, ButtonGroup, Chip, createTheme, Divider, FormControl, FormControlLabel, FormLabel, Grid2, Radio, RadioGroup, Switch, ThemeProvider, useColorScheme } from '@mui/material';

import {ChartLineMultiView, ChartLineView, ChartMultiView, ChartView, DataPoint, DataPointAccelerometer} from '../components/data_display/GraphView';
import {GPSMap} from '../components/data_display/MapView';

import { NavHeader } from '../components/common/nav_header';

import { CommonFloatingToolBox } from '../components/common/common_floating _toolbox';

import GaugeComponent from 'react-gauge-component';
import { Link } from 'react-router-dom';

//const ChartComponent  = <ChartView title="Placeholder Vs. Time" xAxis="Time (Sec)" yAxis="PLACEHOLDER (UNITS)" />
//const MapComponent  = <GPSMap initialCoordinatex={-100} initialCoordinatey={40} />;

import axios from 'axios';
import { render } from '@testing-library/react';

import { GLOBAL_NAMES, GLOBAL_UNITS } from '../App';
import { Global } from '@emotion/react';
import { useStartingParametersStore, Coordinate, useGeneralParametersStore } from '../GlobalStateStores';
import Common from 'electron/common';
import { CommonFloatingInfoBox } from '../components/common/common_floating_infobox';
import { LeafletMap } from '../components/data_display/MapLeafletView';

const Layout = () => {
    const [graphIndex, setGraphIndex] = useState(1);
    const renderState = useGeneralParametersStore((state) => state.renderGUI);
    const [graphNames] = useState(GLOBAL_NAMES);
    const [graphUnits] = useState(GLOBAL_UNITS);

    const [useNewMap, setNewMap] = useState(true);
    const [useAutopan , setAutopan] = useState(false);
    const [map, setMap] = useState(<div></div>);

    function ChartWrapper(ind : number) {
        const [newData, setNewData] = useState([{x:0, y:0, id: 0}]);
        const [newMultiData, setNewMultiData] =useState([{x:0, xx:0, xy: 0, xz: 0, id: "points1"}]);

        useEffect(() => {
            const interval = setInterval(async () => {  
                if (renderState == true){
                    if (graphIndex == 4){
                        var dataSet: DataPointAccelerometer[];
                        dataSet = [];

                        //console.log("Pinging flask server for data on multi axis graph:");
                        await axios.get('http://127.0.0.1:5000/read/graph/all')
                        .then(function (response) {
                            //console.log(accelx[0]);
                            for (let i = 0; i < response.data[4].length; i++){
                                dataSet.push({x: response.data[4][i].x, xx:response.data[4][i].y,  xy:response.data[5][i].y,  xz:response.data[6][i].y, id:(response.data[4][i].id).toString() } )
                            }
                            
                            setNewMultiData(dataSet);
                            
                        })
                        .catch(function (error) {
                            console.log("FAILED TO GET DATA FOR MULTI AXIS ACCELERATION GRAPH, ERROR BELOW: ");
                            console.log(error);
                        });
                    }
                    else{
                        //console.log("Pinging flask server for data on graph of index:" + ind);
                        await axios.get('http://127.0.0.1:5000/read/graph/' + ind)
                            .then(function (response) {
                                //console.log("recieving data on index:" + ind + "Data is:" + response.data[0].toString());
                                setNewData(response.data); //note since we already parsed the data in python into the proper format, no work to be done here
                            })
                            .catch(function (error) {
                                console.log("ERROR IN GRAPH RETRIEVAL OF DATA INDEX: " + ind);
                                console.log(error);
                            });
                        }
                    }


            }, 200);
            
            return () => clearInterval(interval);
        }, [graphIndex, renderState]); //note, [graphIndex] is considered a dependency and thus this interval will be rerendered (with the new graphIndex value) every time graph index changes

        var element;
        if (graphIndex == 4){
            element = [...Array(3).keys()].map((key) => 
            (
                <div>
                    <ChartMultiView title= {graphNames[key+1] + " Graph"} xAxis="Time (Sec)" yAxis = { "Axis Acceleration (G)"} dataset = { newMultiData } graphheight={53.3} pxheight={500} key={key} legend={graphNames[key+1]}></ChartMultiView>            
                </div>  
            ));
        }
        else{
            element = <ChartLineView title="Vs. Time" xAxis= "Time (Sec)" yAxis= {GLOBAL_NAMES[ind] + " ("+ GLOBAL_UNITS[ind] +")"} data = { newData } graphheight={53.3} pxheight={500} legend={GLOBAL_NAMES[graphIndex]}/>
        }
        return element;
    }

    function MapWrapper() {
        const [newCoordinates, setNewCoordinates] = useState(40);
        useEffect(() => {
            if (useNewMap == true){
                setMap(<LeafletMap width='44.5vw' height='53.35vh' freePan = {useAutopan} showBackupMap = {false} key={0}></LeafletMap>) //key forces rerender
            }
            else{
                setMap(<LeafletMap width='44.5vw' height='53.35vh' freePan = {useAutopan} showBackupMap = {true} key={1}></LeafletMap>) //key frces rerender, bad practice, refactor later
                //setMap(<GPSMap key={useAutopan.toString()} initialCoordinatex={-100} initialCoordinatey={newCoordinates} initialLaunchPointCoordinate={useStartingParametersStore.getState().mapStartingMarkerCoordinates} panEnable={useAutopan} />)
            }
        }, [useNewMap, useAutopan]); 

        return null;
    }

    function TextWrapper() {
        const [valueArray, setNewValueArray] = useState([0, 0, 0, 0, 0, 0]);
        const [dictNameMatch] = useState(["Pressure", "Temperature", "Voltage", "X Axis Acceleration","Y Axis Acceleration", "Z Axis Acceleration" , "Latitude", "Longitude"])
        const [dictUnitMatch] = useState(["mBar", "C", "V", "G", "G", "G"])
        
        useEffect(() => {
            const interval = setInterval(async () => {  
                if (renderState == true){
                    //console.log("attempting backend api call for latest text readout data:");
                    await axios.get('http://127.0.0.1:5000/read/last/0')
                    .then(function (response) {
                        //console.log(response.data);
                        setNewValueArray(response.data); //note since we already parsed the data in python into the proper format, no work to be done here
                    })
                    .catch(function (error) {
                        console.log("ERROR IN DATA READ INDEX:");
                        console.log(error);
                    });
                }

            }, 500);

            return () => clearInterval(interval);
        }, [valueArray, renderState]); 
        
        

        return (
            
            [...Array(8).keys()].map((key) => (
                <Card className= "card_readout_home" variant="outlined" key={key}> 
                    {dictNameMatch[key]}
                    <br/>
                    {valueArray[key]}  {dictUnitMatch[key]} 
                </Card>
            ))

        
        
        );
    }

    return (
        <div className='page_container'>


            <CommonFloatingToolBox/>
            <CommonFloatingInfoBox/>
            

            {/*
                <div className='floating_toolbox'>
                <Card className= "card" variant="outlined" >   
                    <div className='page_content'>
                        Radio Status: <br></br>
                        <ButtonGroup variant="contained" aria-label="Stataus">
                            <Button onClick={() => {setRenderState(true);}}> <li> Start GUI </li> </Button>
                            <Button onClick={() => {setRenderState(false);}}> <li> Stop GUI </li> </Button>
                            <Button onClick={() => {}}> <li> Flush Data </li> </Button>
                            <Button onClick={() => {}}> <li> Restart Radio </li> </Button>
                        </ButtonGroup>  
                    </div>    

                </Card>
            </div>
            */}
            
            <NavHeader/>

            <div className='page_content'>
                <div className='overall_container'>
                    
                    <div className="page_title">Dashboard</div>

                    <div className='center_container'>
                        <div className="map_container">
                            {map}
                            {MapWrapper()}
                            <Card className= "card" variant="outlined" >
                                <FormControl >
                                    <FormLabel id="demo-radio-buttons-group-label"> Map Controls</FormLabel>
                                    <RadioGroup
                                        row
                                        aria-labelledby="demo-radio-buttons-group-label"
                                        defaultValue="1"
                                        name="radio-buttons-group" 
                                        >
                                        <FormControlLabel value="1" control={<Switch checked={useAutopan} onChange={() => {setAutopan(!useAutopan)}}/>} label="Enable Panning"  onClick={() => {}} />
                                        <FormControlLabel value="2" control={<Switch checked={useNewMap} onChange={() => {setNewMap(!useNewMap)}}/>} label="Show OSM Map" onClick={() => {}} />
                                    </RadioGroup>
                                </FormControl>
                            </Card>
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
                                        <FormControlLabel value="1" control={<Radio />} label="Pressure"  onClick={() => {setGraphIndex(1);}} />
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