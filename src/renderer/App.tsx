import { MemoryRouter as Router, Routes, Route, Link } from 'react-router-dom';
import icon from '../../assets/start_icon.png';
import './css/App.css';


//page imports for routing
import Home from './Views/PageHome';
import Map from './Views/PageMap';
import Graph from './Views/PageGraph';

//-----


//MUI styling imports
import { Link as MLink} from '@mui/material';

//-----


import {Card} from './components/example_component';

const data  = <Card title="Here is a Example Functional Component" paragraph="Enter main screen below" />


import { ThemeProvider, createTheme } from '@mui/material/styles';


import axios from 'axios';
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
async function initializeRadioConnection() {
  axios.get('http://127.0.0.1:5000/start')
  .then(function (response) {
    console.log("Radio started: ", response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
}

function StartScreen() {
  return (

      <div className="page_container">
          <div className="page_content">
            <div className="section">
              <img width="200" alt="icon" src={icon} />
              
            </div>
            <div className="section"><h1>Groundstation GUI</h1></div>
            <div className="section">
              {data}
            </div>
            <div className="section"> <h2>Debug Menu</h2></div>
            <div className="section">
              <button onClick={() => makeTestPostRequest()}>
                  Flask Test Request
              </button>
               <button onClick={() => initializeRadioConnection()}>
                  Start Radio Connection
              </button>
              <button onClick={() => window.electron.ipcRenderer.sendMessage('start', [''])}>
                  IPC Test Request
              </button>
              </div>
              <div className="floating_section"> <h2>Flask Status</h2> </div>

              <button>
                <li>
                  <Link to="/home">Enter GUI</Link>
                </li>
              </button>

            
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
      </Routes>
    </Router>
      </>
    
  );
}

