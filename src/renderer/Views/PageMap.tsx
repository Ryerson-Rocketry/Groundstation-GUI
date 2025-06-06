import React from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageMap.css';

import Card from '@mui/material/Card';
import { Button } from '@mui/material';

import {ChartView} from '../components/data_display/GraphView';
import {LeafletMap} from '../components/data_display/MapLeafletView';

import { NavHeader } from '../components/common/nav_header';
import { useStartingParametersStore } from '../GlobalStateStores';
import { CommonFloatingToolBox } from '../components/common/common_floating _toolbox';



const Layout = () => {
    return (
        <div className='page_container'>
            <NavHeader/>
            <CommonFloatingToolBox/>
            <div className='page_content_centered_map' style={{marginTop: "50px"}}>
                <Card>
                    <div style={{margin: "10px"}}>
                        <LeafletMap width = "80vw" height ="80vh" freePan= {true} showBackupMap = {true}></LeafletMap>
                    </div>  
                </Card>
                
            </div>
             
        </div>

    )
  };
  
  export default Layout;