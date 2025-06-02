import React, { useEffect, useState } from 'react';
import './../css/App.css';
import './../css/GeneralStyles.css';
import './../css/PageHome.css';
import './../css/PageGraph.css';

import Card from '@mui/material/Card';
import { Button, ButtonGroup } from '@mui/material';

import {ChartView, ChartMultiView, DataPointAccelerometer, DataPoint} from '../components/data_display/GraphView';

import { NavHeader } from '../components/common/nav_header';
import axios from 'axios';

import { GLOBAL_NAMES, GLOBAL_UNITS } from '../App';
import { alignProperty } from '@mui/material/styles/cssUtils';
import { useGeneralParametersStore } from '../GlobalStateStores';
import { CommonFloatingToolBox } from '../components/common/common_floating _toolbox';


const GRAPHHEIGHT = 43;
const GRAPHPXHEIGHT = 400;

const Layout = () => {
    const renderState = useGeneralParametersStore((state) => state.renderGUI);
    const [graphNames] = useState(GLOBAL_NAMES);
    const [graphUnits] = useState(GLOBAL_UNITS);

    function GraphsWrapper() {
        const [newData, setNewData] = useState(
        [[{x:0, y:0, id: 0}],
        [{x:0, y:0, id: 0}],
        [{x:0, y:0, id: 0}]]
    );
    
    
        useEffect(() => {
            const interval = setInterval(async () => {  
                if (renderState == true){
                    await axios.get('http://127.0.0.1:5000/read/graph/all')
                    .then(function (response) {
                        //console.log("recieving data in PageGraph.tsx " + response.data);
                        setNewData(response.data);
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                }

            }, 100);

            return () => clearInterval(interval);
        }, [newData, renderState]); 
        
        

        return (
                [...Array(3).keys()].map((key) => (
                    <div>
                        {graphNames[key] + " Graph"}
                        <ChartView title= {graphNames[key+1] + " Graph"} xAxis="Time (Sec)" yAxis = {graphNames[key+1] + "("+ graphUnits[key+1] + ")"} data = { newData[key+1] } graphheight={GRAPHHEIGHT} pxheight={GRAPHPXHEIGHT} key={key} legend={graphNames[key+1]}></ChartView>            
                    </div>  
                ))

        );
    }

    function AccelerationWrapper() {
        const [newData, setNewData] = useState([{x:0, xx:0, xy: 0, xz: 0, id: "points1"}] );
         useEffect(() => {
            const interval = setInterval(async () => {  
                if (renderState == true){

                    var dataSet: DataPointAccelerometer[];
                    dataSet = [];

                    await axios.get('http://127.0.0.1:5000/read/graph/all')
                    .then(function (response) {

                        
                        //console.log(accelx[0]);
                        for (let i = 0; i < response.data[4].length; i++){
                            
                            dataSet.push({x: response.data[4][i].x, xx:response.data[4][i].y,  xy:response.data[5][i].y,  xz:response.data[6][i].y, id:(response.data[4][i].id).toString() } )
                        }
                        
                        setNewData(dataSet);
                        
                    })
                    .catch(function (error) {
                        console.log(error);
                    });


                }

            }, 100);

            return () => clearInterval(interval);
        }, [newData, renderState]); 

        return (
            <div>Acceleration Graph<ChartMultiView title= {graphNames[4] + " Graph"} xAxis="Time (Sec)" yAxis = {graphNames[4] + "("+ graphUnits[4] + ")"} dataset = { newData } graphheight={GRAPHHEIGHT} pxheight={GRAPHPXHEIGHT} legend={graphNames[3]}></ChartMultiView></div> );
    }
    
    return (
        <div className='page_container'>
            <CommonFloatingToolBox/>

            <NavHeader/>

            
            <div className='page_content'>
                <div className='graphs_container' >
                    {GraphsWrapper()}
                    {AccelerationWrapper()}
                </div>   
            </div>
             
        </div>

    )
  };
  
  export default Layout;