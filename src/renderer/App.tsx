import { MemoryRouter as Router, Routes, Route, Link } from 'react-router-dom';
import icon from '../../assets/start_icon.png';
import './css/App.css';

//page imports for routing
import Home from './Views/PageHome';
import Map from './Views/PageMap';
import Graph from './Views/PageGraph';
import Settings from './Views/PageSettings';

//-----
import { StartScreenFloatingToolbox } from './components/common/start_screen_floating_toolbox';

//MUI styling imports
import { Button, ButtonProps, Chip, Divider, IconButton, Link as MLink, Snackbar, SnackbarCloseReason, styled} from '@mui/material';
//import CloseIcon from '@mui/icons-material/Close'; broken
 
//-----

import { useStartingParametersStore, useStatusStore, Coordinate } from './GlobalStateStores';






import { ThemeProvider, createTheme } from '@mui/material/styles';



import axios from 'axios';
import { CommonFloatingInfoBox } from './components/common/common_floating_infobox';
import { purple } from '@mui/material/colors';
import { LinkButton, RegularButton } from './components/mui_custom_components/mui_custom_component';
import { useState } from 'react';

//TEST FLASK
async function makeTestPostRequest() {
  axios.get('http://127.0.0.1:5000/read/last/0')
  .then(function (response) {
    //console.log("It says: ", response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
}

//Radio
async function initializeFlaskServer() {
  axios.get('http://127.0.0.1:5000/setup')
  .then(function (response) {
    console.log("Flask Setup started: ", response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
}


function StartScreen() {
    const [open, setOpen] = useState(false);

  const handleClick = () => {
    setOpen(true);
  };

  const handleClose = (
  event: React.SyntheticEvent | Event,
  reason?: SnackbarCloseReason,
  ) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  //Radio
  async function initializeRadioConnection(demo: boolean) {
      if (useStatusStore.getState().radioStatus == false){
        if (demo == true){  
          axios.get('http://127.0.0.1:5000/radio/demo')
          .then(function (response) {
            console.log("Radio started: ", response.data);
            useStatusStore.getState().setRadioStatus(true);
          })
          .catch(function (error) {
            console.log(error);
          });
        } 
        else{
          axios.get('http://127.0.0.1:5000/radio/start')
          .then(function (response) {
            console.log("Radio started in demo mode: ", response.data);
            useStatusStore.getState().setRadioStatus(true);
          })
          .catch(function (error) {
            console.log(error);
          });
        }


    }
    else{
      console.log("radio already running");
      setOpen(true);
    }
    
  }

  return (

      <div className="page_container">

        <Snackbar
          open={open}
          autoHideDuration={1000}
          onClose={handleClose}
          message="Radio already running!"
        />
          


        <StartScreenFloatingToolbox/>
        <CommonFloatingInfoBox/>

          <div className="page_content">
            <div className="section">
              <img width="200" alt="icon" src={icon} />
              
            </div>
            <div className="section"><h1>Groundstation GUI</h1></div>

            <div className="section"> <h2>Initialization Menu</h2></div>
            <Divider component="li"> <Chip label="Radio Setup" size="small" /></Divider>
            <div className="section">
              <RegularButton onClick={() => initializeRadioConnection(false)}> 
                  Start Radio Connection
              </RegularButton>
              <RegularButton onClick={() => initializeRadioConnection(true)}> 
                  Start Demo Mode
              </RegularButton>
              {/*
                <button onClick={() => window.electron.ipcRenderer.sendMessage('start', [''])}>
                  IPC Test Request
                </button>
              */}

              </div>
            <Divider component="li"> </Divider>
              <div className="section">
                <LinkButton component={Link} to={'/home'} variant="contained"> Enter Dashboard </LinkButton>
              </div>
            
        </div>
      </div>

    
  );
}

const theme = createTheme({
  colorSchemes: {
    dark: true,
  },
  components: {
  MuiButtonBase: {
    defaultProps: {
      
    }
  }
  
  }
});


export default function App() {
  return (
    <>
    <Router>
      <Routes>
        <Route path="/" element={<ThemeProvider theme={theme}><StartScreen /></ThemeProvider>} />
        <Route path="/home" element={<ThemeProvider theme={theme}><Home /></ThemeProvider>} />
        <Route path="/map" element={<ThemeProvider theme={theme}><Map /></ThemeProvider>} />
        <Route path="/graph" element={<ThemeProvider theme={theme}><Graph /></ThemeProvider>} />
        <Route path="/settings" element={<ThemeProvider theme={theme}><Settings /></ThemeProvider>} />
      </Routes>
    </Router>
      </>
    
  );
}


export const GLOBAL_NAMES = ["Time", "Pressure", "Temperature", "Voltage", "X Axis Acceleration","Y Axis Acceleration", "Z Axis Acceleration"];
export const GLOBAL_UNITS = ["Sec", "mBar", "C", "V", "G", "G", "G"];

