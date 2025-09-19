import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Grid,
  Button,
} from '@mui/material';
import { Editor } from '@monaco-editor/react';

interface StepDefinitionContent {
  step_definitions: Record<string, string>;
  imports: string[];
  setup_code?: string;
}

const StepDefinitionGenerator = () => {
  const [featureContent, setFeatureContent] = useState('');
  const [language, setLanguage] = useState('');
  const [framework, setFramework] = useState('');
  const [stepDefinitions, setStepDefinitions] = useState<StepDefinitionContent | null>(null);

  const handleSubmit = async () => {
    if (!featureContent || !language) return;

    try {
      const response = await fetch('http://localhost:8000/api/generate-steps', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          feature_content: featureContent,
          programming_language: language,
          framework,
        }),
      });

      const data = await response.json();
      setStepDefinitions(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box mt={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Feature File Content
              </Typography>
              <Box mt={2} height="300px">
                <Editor
                  height="100%"
                  defaultLanguage="gherkin"
                  defaultValue={featureContent}
                  onChange={(value) => setFeatureContent(value || '')}
                  options={{
                    minimap: { enabled: false },
                  }}
                />
              </Box>
              <Box mt={3}>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <FormControl fullWidth>
                      <InputLabel>Programming Language</InputLabel>
                      <Select
                        value={language}
                        label="Programming Language"
                        onChange={(e) => setLanguage(e.target.value)}
                      >
                        <MenuItem value="python">Python</MenuItem>
                        <MenuItem value="javascript">JavaScript</MenuItem>
                        <MenuItem value="java">Java</MenuItem>
                        <MenuItem value="csharp">C#</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={6}>
                    <FormControl fullWidth>
                      <InputLabel>Framework</InputLabel>
                      <Select
                        value={framework}
                        label="Framework"
                        onChange={(e) => setFramework(e.target.value)}
                      >
                        <MenuItem value="behave">Behave (Python)</MenuItem>
                        <MenuItem value="cucumber">Cucumber (JS/Java/C#)</MenuItem>
                        <MenuItem value="pytest-bdd">Pytest-BDD (Python)</MenuItem>
                        <MenuItem value="jest-cucumber">Jest-Cucumber (JavaScript)</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
              </Box>
              <Box mt={3}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                  disabled={!featureContent || !language}
                >
                  Generate Step Definitions
                </Button>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Generated Step Definitions
              </Typography>
              <Box mt={2} height="500px">
                {stepDefinitions ? (
                  <Editor
                    height="100%"
                    defaultLanguage={language.toLowerCase()}
                    defaultValue={Object.values(stepDefinitions.step_definitions).join('\n\n')}
                    options={{
                      minimap: { enabled: false },
                      readOnly: false,
                    }}
                  />
                ) : (
                  <Typography color="textSecondary">
                    Generated step definitions will appear here
                  </Typography>
                )}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default StepDefinitionGenerator;