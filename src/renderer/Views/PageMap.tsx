import React from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageHome.css';

import Card from '@mui/material/Card';
import { Button } from '@mui/material';

import {ChartView} from '../components/data_display/GraphView';
import {GPSMap} from '../components/data_display/MapView';

import { NavHeader } from '../components/common/nav_header';

const MapComponent  = <GPSMap initialCoordinatex={-100} initialCoordinatey={40} />;


const Layout = () => {
    return (
        <div className='page_container'>
            <NavHeader/>
            <div className='page_content'>
            
            </div>
             
        </div>

    )
  };
  
  export default Layout;