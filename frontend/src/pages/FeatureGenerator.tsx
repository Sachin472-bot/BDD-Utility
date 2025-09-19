import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Grid,
} from '@mui/material';
import { Editor } from '@monaco-editor/react';

interface FeatureContent {
  feature_content: string;
  suggested_steps: Record<string, any>;
}

const FeatureGenerator = () => {
  const [file, setFile] = useState<File | null>(null);
  const [docType, setDocType] = useState('');
  const [featureContent, setFeatureContent] = useState<FeatureContent | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file || !docType) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('doc_type', docType);

    try {
      const response = await fetch('http://localhost:8000/api/convert-to-feature', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setFeatureContent(data);
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
                Upload Document
              </Typography>
              <Box mt={2}>
                <input
                  accept=".docx,.pdf,.txt"
                  id="document-upload"
                  type="file"
                  style={{ display: 'none' }}
                  onChange={handleFileUpload}
                />
                <label htmlFor="document-upload">
                  <Button variant="contained" component="span">
                    Choose File
                  </Button>
                </label>
                {file && <Typography mt={1}>{file.name}</Typography>}
              </Box>
              <Box mt={3}>
                <FormControl fullWidth>
                  <InputLabel>Document Type</InputLabel>
                  <Select
                    value={docType}
                    label="Document Type"
                    onChange={(e) => setDocType(e.target.value)}
                  >
                    <MenuItem value="BRD">Business Requirements Document</MenuItem>
                    <MenuItem value="FRD">Functional Requirements Document</MenuItem>
                    <MenuItem value="User Story">User Story</MenuItem>
                    <MenuItem value="Test Case">Test Case</MenuItem>
                  </Select>
                </FormControl>
              </Box>
              <Box mt={3}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                  disabled={!file || !docType}
                >
                  Generate Feature File
                </Button>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, minHeight: '400px' }}>
              <Typography variant="h5" gutterBottom>
                Generated Feature File
              </Typography>
              <Box mt={2} height="400px">
                {featureContent ? (
                  <Editor
                    height="100%"
                    defaultLanguage="gherkin"
                    defaultValue={featureContent.feature_content}
                    options={{
                      minimap: { enabled: false },
                      readOnly: false,
                    }}
                  />
                ) : (
                  <Typography color="textSecondary">
                    Generated feature file will appear here
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

export default FeatureGenerator;