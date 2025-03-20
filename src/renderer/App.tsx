import { MemoryRouter as Router, Routes, Route, Link } from 'react-router-dom';
import icon from '../../assets/start_icon.png';
import './css/App.css';


//page imports for routing
import Home from './PageHome';
import Map from './PageMap';

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
  axios.get('http://127.0.0.1:5000/test')
  .then(function (response) {
    console.log("It says: ", response.data);
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
            <div className="section"><h1>Groundstation GUI Test</h1></div>
            <div className="section">
              {data}
            </div>
            <div className="section">
              <button onClick={() => makeTestPostRequest()}>
                  Flask Test Request
              </button>
              <button>
                <li>
                  <Link to="/home">Enter GUI</Link>
                </li>
              </button>

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
      </Routes>
    </Router>
      </>
    
  );
}

