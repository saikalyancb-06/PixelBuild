import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  TextField,
  CircularProgress,
  Alert,
  IconButton,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  Upload as UploadIcon,
  Download as DownloadIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayIcon,
  CheckCircle,
  Warning,
} from '@mui/icons-material';
import axios from 'axios';
import RiskBadge from '../components/RiskBadge';
import { useNotification } from '../components/NotificationContext';

export default function Scans() {
  const [urls, setUrls] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const { showNotification } = useNotification();

  const handleBatchCheck = async () => {
    const urlList = urls.split('\n').filter(url => url.trim() !== '');
    
    if (urlList.length === 0) {
      showNotification('Please enter at least one URL', 'warning');
      return;
    }

    if (urlList.length > 50) {
      showNotification('Maximum 50 URLs allowed per batch', 'error');
      return;
    }

    setLoading(true);
    setProgress(0);
    setResults([]);

    const batchResults = [];
    const total = urlList.length;

    for (let i = 0; i < urlList.length; i++) {
      try {
        const response = await axios.post('http://localhost:8000/api/quick-check', {
          url: urlList[i].trim()
        });
        batchResults.push({
          url: urlList[i].trim(),
          ...response.data,
          status: 'success'
        });
      } catch (error) {
        batchResults.push({
          url: urlList[i].trim(),
          status: 'error',
          error: error.response?.data?.detail || 'Failed to check',
          app_name: 'Error',
          package_id: 'N/A',
          risk_score: 0,
          is_fake: false
        });
      }
      setProgress(Math.round(((i + 1) / total) * 100));
      setResults([...batchResults]);
    }

    setLoading(false);
    showNotification(`Batch check complete: ${batchResults.length} URLs processed`, 'success');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      // Parse CSV (simple comma or newline separated)
      const lines = text.split(/[\n,]/).map(line => line.trim()).filter(line => line);
      setUrls(lines.join('\n'));
      showNotification(`Loaded ${lines.length} URLs from file`, 'info');
    };
    reader.readAsText(file);
  };

  const downloadResults = () => {
    if (results.length === 0) {
      showNotification('No results to download', 'warning');
      return;
    }

    // Create CSV
    const headers = ['URL', 'App Name', 'Package ID', 'Developer', 'Risk Score', 'Is Fake', 'Status'];
    const rows = results.map(r => [
      r.url,
      r.app_name || 'N/A',
      r.package_id || 'N/A',
      r.developer || 'N/A',
      r.risk_score || 0,
      r.is_fake ? 'FAKE' : 'SAFE',
      r.status
    ]);

    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `batch_scan_results_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Results downloaded successfully', 'success');
  };

  const clearResults = () => {
    setResults([]);
    setProgress(0);
    showNotification('Results cleared', 'info');
  };

  return (
    <Box>
      <Box mb={3}>
        <Typography variant="h4" gutterBottom sx={{ 
          fontWeight: 'bold',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          Batch URL Scanner
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Check multiple app URLs at once (max 50 per batch)
        </Typography>
      </Box>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Enter URLs to Check
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Enter one URL per line, or upload a CSV/text file
        </Typography>

        <TextField
          fullWidth
          multiline
          rows={10}
          placeholder={`https://play.google.com/store/apps/details?id=com.example.app1\nhttps://play.google.com/store/apps/details?id=com.example.app2\nhttps://play.google.com/store/apps/details?id=com.example.app3`}
          value={urls}
          onChange={(e) => setUrls(e.target.value)}
          disabled={loading}
          variant="outlined"
          sx={{ mb: 2, fontFamily: 'monospace' }}
        />

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Button
            variant="contained"
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <PlayIcon />}
            onClick={handleBatchCheck}
            disabled={loading || !urls.trim()}
          >
            {loading ? `Checking... ${progress}%` : 'Start Batch Check'}
          </Button>

          <Button
            variant="outlined"
            component="label"
            startIcon={<UploadIcon />}
            disabled={loading}
          >
            Upload File
            <input
              type="file"
              hidden
              accept=".csv,.txt"
              onChange={handleFileUpload}
            />
          </Button>

          <Typography variant="body2" color="text.secondary">
            {urls.split('\n').filter(u => u.trim()).length} URLs entered
          </Typography>
        </Box>

        {loading && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress variant="determinate" value={progress} />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
              Processing {Math.round((progress / 100) * urls.split('\n').filter(u => u.trim()).length)} of {urls.split('\n').filter(u => u.trim()).length} URLs
            </Typography>
          </Box>
        )}
      </Paper>

      {results.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Scan Results ({results.length} apps)
            </Typography>
            <Box>
              <Tooltip title="Download as CSV">
                <IconButton onClick={downloadResults} color="primary">
                  <DownloadIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Clear Results">
                <IconButton onClick={clearResults} color="error">
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>

          <Alert severity="info" sx={{ mb: 2 }}>
            {results.filter(r => r.is_fake).length} fake apps detected out of {results.length} checked
          </Alert>

          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>#</TableCell>
                  <TableCell>App Name</TableCell>
                  <TableCell>Package ID</TableCell>
                  <TableCell>Risk Score</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>URL</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {results.map((result, index) => (
                  <TableRow 
                    key={index}
                    sx={{ backgroundColor: result.is_fake ? '#ffebee' : 'inherit' }}
                  >
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>
                      {result.status === 'error' ? (
                        <Typography color="error" variant="body2">
                          Error
                        </Typography>
                      ) : (
                        <>
                          {result.is_fake ? (
                            <Warning sx={{ color: '#f44336', fontSize: 20, mr: 1, verticalAlign: 'middle' }} />
                          ) : (
                            <CheckCircle sx={{ color: '#4caf50', fontSize: 20, mr: 1, verticalAlign: 'middle' }} />
                          )}
                          {result.app_name}
                        </>
                      )}
                    </TableCell>
                    <TableCell sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                      {result.package_id}
                    </TableCell>
                    <TableCell>
                      {result.status === 'success' && (
                        <RiskBadge riskScore={result.risk_score} size="small" />
                      )}
                    </TableCell>
                    <TableCell>
                      {result.status === 'success' ? (
                        <Chip 
                          label={result.is_fake ? 'FAKE' : 'SAFE'} 
                          color={result.is_fake ? 'error' : 'success'}
                          size="small"
                        />
                      ) : (
                        <Chip label="ERROR" color="error" size="small" />
                      )}
                    </TableCell>
                    <TableCell>
                      <Tooltip title={result.url}>
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            maxWidth: 200, 
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            display: 'block'
                          }}
                        >
                          {result.url}
                        </Typography>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}
    </Box>
  );
}
