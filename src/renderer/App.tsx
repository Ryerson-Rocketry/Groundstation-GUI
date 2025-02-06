import { MemoryRouter as Router, Routes, Route, Link } from 'react-router-dom';
import icon from '../../assets/start_icon.png';
import './App.css';


//page imports for routing
import Home from './PageHome';

//-----


//MUI styling imports
import { Link as MLink} from '@mui/material';

//-----


import {Card} from './components/example_component';

const data  = <Card title="Here is a Example Functional Component" paragraph="Enter main screen below" />


function StartScreen() {
  return (


      <div className="container">
        <div className="section">
          <img width="200" alt="icon" src={icon} />
        </div>
        <div className="section"><h1>Groundstation GUI Test</h1></div>
        <div className="section">
          {data}
        </div>
        <div className="section">
          <button>
            <li>
              <Link to="/home">Enter GUI</Link>
            </li>
          </button>

        </div>
      </div>

    
  );
}

export default function App() {
  return (


    
    <Router>
      <Routes>
        <Route path="/" element={<StartScreen />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

