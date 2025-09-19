import React from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';

const Home = () => {
  return (
    <Container maxWidth="md">
      <Box mt={4}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Welcome to BDD Utility
          </Typography>
          <Typography variant="body1" paragraph>
            This tool helps you convert various requirement documents (BRD, FRD, User Stories,
            Test Cases) into Gherkin feature files and generate step definitions for your
            chosen programming language.
          </Typography>
          <Typography variant="h6" gutterBottom>
            Features:
          </Typography>
          <ul>
            <li>Convert requirement documents to Gherkin format</li>
            <li>Support for BRD, FRD, User Stories, and Test Cases</li>
            <li>Generate step definitions in multiple programming languages</li>
            <li>Intelligent NLP-based conversion</li>
            <li>Real-time preview and editing</li>
          </ul>
        </Paper>
      </Box>
    </Container>
  );
};

export default Home;