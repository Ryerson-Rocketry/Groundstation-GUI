import { Button, ButtonGroup, Card, Chip, Divider, Grid2 } from '@mui/material';
import '../../css/GeneralStyles.css';
import React from 'react';
import { Link } from 'react-router-dom';



export const NavHeader = () => <aside>
  <div className='header_container'>   

    <div className='header_info_section'>  
      <ButtonGroup variant="contained" aria-label="Basic button group">
        <Button> <li> <Link to="/">Start Menu</Link> </li> </Button>
        <Button> <li> <Link to="/home">Home Dashboard</Link> </li> </Button>
        <Button> <li> <Link to="/graph">Graph</Link> </li> </Button>
        <Button> <li> <Link to="/map">GPS Map</Link> </li> </Button>
        <Button> <li> <Link to="/config">Settings</Link> </li> </Button>
      </ButtonGroup>  

      <Grid2 container spacing={2}>
      <Grid2 size={8}>
        <Card>GUI Status</Card>
      </Grid2>
    </Grid2>
    </div>  
     
      
    <Divider component="li"> <Chip label="Nav Bar" size="small" /></Divider>
  </div>             
    
</aside>
  