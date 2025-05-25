import React, { useEffect, useState } from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageHome.css';

import Card from '@mui/material/Card';
import { Button } from '@mui/material';

import {ChartView} from '../components/data_display/GraphView';

import { NavHeader } from '../components/common/nav_header';
import axios from 'axios';


const Layout = () => {
    const [renderState, setRenderState] = useState(false);

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
            <NavHeader/>
            <div className='page_content'>
            
            </div>
             
        </div>

    )
  };
  
  export default Layout;