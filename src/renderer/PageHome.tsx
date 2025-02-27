import React from 'react';
import './css/App.css';
import './css/GeneralStyles.css';
import './css/PageHome.css';

import Card from '@mui/material/Card';
import { Button, createTheme, FormControl, FormControlLabel, FormLabel, Radio, RadioGroup, ThemeProvider, useColorScheme } from '@mui/material';

import {Chart} from './components/data_display/graph';
import {GPSMap} from './components/data_display/map';

import { NavHeader } from './components/common/nav_header';

import GaugeComponent from 'react-gauge-component';
import { Link } from 'react-router-dom';

const ChartComponent  = <Chart title="Placeholder Vs. Time" xAxis="Time (Sec)" yAxis="PLACEHOLDER (UNITS)" />
const MapComponent  = <GPSMap initialCoordinatex={-100} initialCoordinatey={40} />;




const Layout = () => {
    return (

        <div className='page_container'>
            
            <NavHeader/>

            <div className='page_content'>
                <div className='overall_container'>
                    <div className="page_title">Dashboard</div>
                                    
                    <div className='center_container'>
                        <div className="map_container">
                            {MapComponent}
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
                                        <FormControlLabel value="1" control={<Radio />} label="Pressure" />
                                        <FormControlLabel value="2" control={<Radio />} label="Temperature" />
                                        <FormControlLabel value="3" control={<Radio />} label="Voltage" />
                                        <FormControlLabel value="4" control={<Radio />} label="Acceleration" />
                                    </RadioGroup>
                                </FormControl>
      
                            </Card>
                            {ChartComponent} 
                        </div>    
                    </div>

                    <div className='bottom_container'>
                        <Card className= "card" variant="outlined" >
                            <div className="gauge_row">                           
                                <GaugeComponent />
                                <GaugeComponent />
                                <GaugeComponent />
                                <GaugeComponent />
                                <GaugeComponent />

                            </div>
                        </Card>
                    </div>


                </div>
            </div>

             
            
        </div>
    )
  };
  
  export default Layout;