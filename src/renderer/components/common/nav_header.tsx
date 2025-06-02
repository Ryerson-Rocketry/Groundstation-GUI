import { Button, ButtonGroup, Card, Chip, Divider, Grid2 } from '@mui/material';
import '../../css/GeneralStyles.css';
import React from 'react';
import { Link } from 'react-router-dom';
import { LinkButton } from '../mui_custom_components/mui_custom_component';



export const NavHeader = () => <aside>
  <div className='header_container'>   

    <div className='header_info_section'>  
      
      <ButtonGroup variant="contained" aria-label="Basic button group">
        <LinkButton component={Link} to={'/'} variant="contained">Start Menu</LinkButton>
        <LinkButton component={Link} to={'/home'} variant="contained">Home Dashboard</LinkButton>
        <LinkButton component={Link} to={'/graph'} variant="contained">Graph</LinkButton>
        <LinkButton component={Link} to={'/map'} variant="contained">GPS Map</LinkButton>
        <LinkButton component={Link} to={'/settings'} variant="contained">Settings</LinkButton>
      </ButtonGroup>  
    </div>  
     
      
    <Divider component="li"> <Chip label="Nav Bar" size="small" /></Divider>
  </div>             
    
</aside>
  