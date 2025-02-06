import React from 'react';
import './App.css';
import './GeneralStyles.css';
import './PageHome.css';

import Card from '@mui/material/Card';
import { Button } from '@mui/material';

import {Chart} from './components/data_display/graph';
import {GPSMap} from './components/data_display/map';

import GaugeComponent from 'react-gauge-component';

const ChartComponent  = <Chart title="Placeholder Vs. Time" xAxis="Time (Sec)" yAxis="PLACEHOLDER (UNITS)" />
const MapComponent  = <GPSMap title="" xAxis="Time (Sec)" />

const Layout = () => {
    return (
        <div className='page_container'>

            <div className='overall_container'>
                <div className="home_header">Groundstation GUI Test</div>
                                
                <div className='center_container'>
                    <Card className= "card" variant="outlined">
                    {MapComponent}
                    </Card>

                    <Card className= "card" variant="outlined">
                        <div className="graph_component">
                            <div className="graph_button_row">
                                <Button>Graph 1</Button>
                                <Button>Graph 2</Button>
                                <Button>Graph 3</Button>
                                <Button>Graph 4</Button>
                                <Button>Graph 5</Button>
                            </div>
                           {ChartComponent} 
                        </div>
                    </Card>
                    
                </div>

                <Card className= "card" variant="outlined" >
                    <div className="bottom_container">
                    
                        <GaugeComponent />
                        <GaugeComponent />
                        <GaugeComponent />
                        <GaugeComponent />
                        <GaugeComponent />


                    </div>
                </Card>

            </div>
             
            
        </div>
    )
  };
  
  export default Layout;