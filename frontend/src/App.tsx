import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from './theme';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import FeatureGenerator from './pages/FeatureGenerator';
import StepDefinitionGenerator from './pages/StepDefinitionGenerator';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/feature-generator" element={<FeatureGenerator />} />
        <Route path="/step-definitions" element={<StepDefinitionGenerator />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;