import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Navigation = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          BDD Utility
        </Typography>
        <Button color="inherit" component={RouterLink} to="/">
          Home
        </Button>
        <Button color="inherit" component={RouterLink} to="/feature-generator">
          Generate Feature
        </Button>
        <Button color="inherit" component={RouterLink} to="/step-definitions">
          Generate Steps
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;