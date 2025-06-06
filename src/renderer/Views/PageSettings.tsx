import React from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageSetting.css';

import Card from '@mui/material/Card';
import { Button } from '@mui/material';

import {ChartView} from '../components/data_display/GraphView';
import {LeafletMap} from '../components/data_display/MapLeafletView';

import { NavHeader } from '../components/common/nav_header';
import { useStartingParametersStore } from '../GlobalStateStores';
import { CommonFloatingToolBox } from '../components/common/common_floating _toolbox';
import { CommonFloatingInfoBox } from '../components/common/common_floating_infobox';
import { LinkButton, RegularButton } from '../components/mui_custom_components/mui_custom_component';
import { Link } from 'react-router-dom';

function OpenNewWindow(){
    window.open('https://github.com/Ryerson-Rocketry/Groundstation-GUI/tree/Electron_Conversion', '_blank', 'top=500,left=200,frame=false,nodeIntegration=no')
}

const Layout = () => {
    return (

        <div className='page_container'>
            
            <CommonFloatingToolBox/>
            <CommonFloatingInfoBox/>
            <NavHeader/>

            <div className='center_container_settings'>
                <Card style={{width: "35vw"}}>
                    Settings

                    <Card> 
                        About 
                        <div className='element_row_settings'> Github Repo: <Card className= "card_right_align" variant="outlined">  <RegularButton onClick={() => OpenNewWindow()}>Link</RegularButton> </Card> </div>
                        <div className='element_row_settings'> GUI Version:   <Card className= "card_right_align" variant="outlined">V 1.0</Card> </div>
                        <div className='element_row_settings'> Flask Version:  <Card className= "card_right_align" variant="outlined">V 1.0</Card> </div>
                    </Card>
                    
                </Card>
                
            </div>
             
        </div>



    )
  };
  
  export default Layout;