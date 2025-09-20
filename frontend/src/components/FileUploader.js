import React, { useState, useCallback } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  Alert,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';

const FileUploader = ({ onFeatureGenerated, onError }) => {
  const [file, setFile] = useState(null);
  const [fileFormat, setFileFormat] = useState('');
  const [docType, setDocType] = useState('');
  const [suggestedType, setSuggestedType] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const format = uploadedFile.name.split('.').pop().toLowerCase();
      setFileFormat(format);
      
      // Analyze document type
      setIsAnalyzing(true);
      try {
        const formData = new FormData();
        formData.append('file', uploadedFile);
        
        const response = await fetch('/api/conversion/analyze', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          throw new Error('Failed to analyze document');
        }
        
        const data = await response.json();
        if (data.suggested_type) {
          setSuggestedType(data.suggested_type);
          setDocType(data.suggested_type);
        }
      } catch (error) {
        onError('Error analyzing document: ' + error.message);
      } finally {
        setIsAnalyzing(false);
      }
    }
  }, [onError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  const handleGenerateFeature = async () => {
    if (!file) {
      onError('Please upload a file first');
      return;
    }

    setIsGenerating(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (docType) {
        formData.append('doc_type', docType);
      }

      const response = await fetch('/api/convert-to-feature', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to generate feature file');
      }

      const data = await response.json();
      onFeatureGenerated(data);
    } catch (error) {
      onError('Error generating feature file: ' + error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Box
          {...getRootProps()}
          sx={{
            border: '2px dashed #ccc',
            borderRadius: 2,
            p: 3,
            textAlign: 'center',
            mb: 2,
            cursor: 'pointer',
            '&:hover': {
              borderColor: 'primary.main',
            },
          }}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <Typography>Drop the file here ...</Typography>
          ) : (
            <Typography>
              Drag & drop a file here, or click to select
              <br />
              <small>(Supported formats: PDF, DOCX, TXT)</small>
            </Typography>
          )}
        </Box>

        {file && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              File: {file.name}
            </Typography>
            
            {isAnalyzing ? (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <CircularProgress size={20} />
                <Typography>Analyzing document...</Typography>
              </Box>
            ) : (
              <>
                {suggestedType && (
                  <Alert severity="info" sx={{ mb: 2 }}>
                    Suggested document type: {suggestedType}
                  </Alert>
                )}
                
                <FormControl fullWidth margin="normal">
                  <InputLabel>Document Type</InputLabel>
                  <Select
                    value={docType}
                    label="Document Type"
                    onChange={(e) => setDocType(e.target.value)}
                  >
                    <MenuItem value="BRD">Business Requirements Document (BRD)</MenuItem>
                    <MenuItem value="FRD">Functional Requirements Document (FRD)</MenuItem>
                    <MenuItem value="User Story">User Story</MenuItem>
                    <MenuItem value="Test Case">Test Case</MenuItem>
                  </Select>
                </FormControl>

                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleGenerateFeature}
                  disabled={!docType || isGenerating}
                  fullWidth
                  sx={{ mt: 2 }}
                >
                  {isGenerating ? (
                    <>
                      <CircularProgress size={20} sx={{ mr: 1 }} />
                      Generating Feature File...
                    </>
                  ) : (
                    'Generate Feature File'
                  )}
                </Button>
              </>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default FileUploader;