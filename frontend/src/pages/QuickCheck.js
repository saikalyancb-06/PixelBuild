import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Grid,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Search as SearchIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Shield as ShieldIcon,
  Refresh as RefreshIcon,
  History as HistoryIcon
} from '@mui/icons-material';
import axios from 'axios';
import RiskBadge from '../components/RiskBadge';
import { useNotification } from '../components/NotificationContext';

const QuickCheck = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [recentChecks, setRecentChecks] = useState([]);
  const { showNotification } = useNotification();

  // Load recent checks from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('recentChecks');
    if (saved) {
      try {
        setRecentChecks(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to load recent checks:', e);
      }
    }
  }, []);

  // Save recent check to history
  const saveRecentCheck = (checkData) => {
    const newCheck = {
      url: checkData.url || url,
      app_name: checkData.app_name,
      package_id: checkData.package_id,
      risk_score: checkData.risk_score,
      is_fake: checkData.is_fake,
      timestamp: new Date().toISOString()
    };
    
    const updated = [newCheck, ...recentChecks.filter(c => c.package_id !== newCheck.package_id)].slice(0, 5);
    setRecentChecks(updated);
    localStorage.setItem('recentChecks', JSON.stringify(updated));
  };

  const getRiskColor = (score) => {
    if (score >= 90) return '#d32f2f'; // Red - Critical
    if (score >= 70) return '#f57c00'; // Orange - High
    if (score >= 50) return '#fbc02d'; // Yellow - Medium
    return '#388e3c'; // Green - Low
  };

  const getRiskLevel = (score) => {
    if (score >= 90) return 'CRITICAL';
    if (score >= 70) return 'HIGH';
    if (score >= 50) return 'MEDIUM';
    return 'LOW';
  };

  const handleCheck = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/quick-check', {
        url: url.trim()
      });
      
      setResult(response.data);
      saveRecentCheck({ ...response.data, url: url.trim() });
      
      // Show success notification
      if (response.data.is_fake) {
        showNotification(`⚠️ Fake app detected: ${response.data.app_name}`, 'error');
      } else {
        showNotification(`✓ ${response.data.app_name} appears legitimate`, 'success');
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to check the URL. Please try again.';
      setError(errorMsg);
      showNotification(errorMsg, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleCheck();
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <ShieldIcon sx={{ fontSize: 60, color: '#667eea', mb: 2 }} />
          <Typography variant="h4" gutterBottom sx={{ 
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            Is This App Real or Fake?
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Paste any Google Play Store URL to verify authenticity instantly
          </Typography>
        </Box>

        {/* Search Box */}
        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Paste app URL here (e.g., https://play.google.com/store/apps/details?id=com.example.app)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
            InputProps={{
              sx: { fontSize: '1.1rem' }
            }}
          />
          <Button
            fullWidth
            variant="contained"
            size="large"
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
            onClick={handleCheck}
            disabled={loading || !url.trim()}
            sx={{ mt: 2, py: 1.5, fontSize: '1.1rem' }}
          >
            {loading ? 'Checking...' : 'Check This App'}
          </Button>
        </Box>

        {/* Recent Checks */}
        {recentChecks.length > 0 && !result && (
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <HistoryIcon sx={{ mr: 1, color: '#667eea' }} />
              <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                Recent Checks
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {recentChecks.map((check, index) => (
                <Tooltip key={index} title={`Checked ${new Date(check.timestamp).toLocaleString()}`}>
                  <Chip
                    label={check.app_name}
                    size="small"
                    color={check.is_fake ? 'error' : 'success'}
                    variant="outlined"
                    icon={check.is_fake ? <WarningIcon /> : <CheckCircleIcon />}
                    onClick={() => {
                      setUrl(`https://play.google.com/store/apps/details?id=${check.package_id}`);
                      showNotification('URL loaded from history', 'info');
                    }}
                    deleteIcon={<RefreshIcon />}
                    onDelete={() => {
                      setUrl(`https://play.google.com/store/apps/details?id=${check.package_id}`);
                      handleCheck();
                    }}
                    sx={{ cursor: 'pointer' }}
                  />
                </Tooltip>
              ))}
            </Box>
          </Box>
        )}

        {/* Error Message */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Results */}
        {result && (
          <Card 
            elevation={4} 
            sx={{ 
              mt: 3, 
              border: `3px solid ${getRiskColor(result.risk_score)}`,
              backgroundColor: result.is_fake ? '#ffebee' : '#e8f5e9'
            }}
          >
            <CardContent>
              {/* Main Verdict */}
              <Box sx={{ textAlign: 'center', mb: 3 }}>
                {result.is_fake ? (
                  <>
                    <ErrorIcon sx={{ fontSize: 80, color: '#d32f2f', mb: 1 }} />
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#d32f2f' }}>
                      ⚠️ FAKE APP DETECTED!
                    </Typography>
                    <Typography variant="h6" color="error" sx={{ mt: 1 }}>
                      DO NOT INSTALL - This app appears to be counterfeit
                    </Typography>
                  </>
                ) : (
                  <>
                    <CheckCircleIcon sx={{ fontSize: 80, color: '#388e3c', mb: 1 }} />
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#388e3c' }}>
                      ✓ Looks Legitimate
                    </Typography>
                    <Typography variant="h6" sx={{ color: '#388e3c', mt: 1 }}>
                      This app appears to be authentic
                    </Typography>
                  </>
                )}
              </Box>

              <Divider sx={{ my: 3 }} />

              {/* App Details */}
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    App Information:
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    App Name
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                    {result.app_name}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Package ID
                  </Typography>
                  <Typography variant="body1" sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>
                    {result.package_id}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Developer
                  </Typography>
                  <Typography variant="body1">
                    {result.developer}
                  </Typography>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Store
                  </Typography>
                  <Typography variant="body1">
                    {result.store}
                  </Typography>
                </Grid>
              </Grid>

              <Divider sx={{ my: 3 }} />

              {/* Risk Score with Badge */}
              <Box sx={{ textAlign: 'center', my: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Risk Assessment
                </Typography>
                <RiskBadge riskScore={result.risk_score} size="medium" />
              </Box>

              <Divider sx={{ my: 3 }} />
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Risk Assessment:
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <Chip 
                    label={`Risk Level: ${getRiskLevel(result.risk_score)}`}
                    sx={{ 
                      backgroundColor: getRiskColor(result.risk_score),
                      color: 'white',
                      fontWeight: 'bold',
                      fontSize: '1rem',
                      py: 2
                    }}
                  />
                  <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                    {result.risk_score}%
                  </Typography>
                </Box>
                <Box sx={{ 
                  height: 20, 
                  backgroundColor: '#e0e0e0', 
                  borderRadius: 2,
                  overflow: 'hidden'
                }}>
                  <Box sx={{
                    height: '100%',
                    width: `${result.risk_score}%`,
                    backgroundColor: getRiskColor(result.risk_score),
                    transition: 'width 0.5s ease'
                  }} />
                </Box>
              </Box>

              {/* Detection Reasons */}
              {result.reasons && result.reasons.length > 0 && (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Why is this suspicious?
                  </Typography>
                  {result.reasons.map((reason, index) => (
                    <Alert 
                      key={index} 
                      severity={result.is_fake ? "error" : "warning"}
                      icon={<WarningIcon />}
                      sx={{ mb: 1 }}
                    >
                      {reason}
                    </Alert>
                  ))}
                </Box>
              )}

              {/* Recommendation */}
              <Box sx={{ mt: 3, p: 2, backgroundColor: result.is_fake ? '#ffcdd2' : '#c8e6c9', borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Recommendation:
                </Typography>
                <Typography variant="body1">
                  {result.is_fake ? (
                    <>
                      <strong>DO NOT install this app.</strong> It appears to be impersonating a legitimate app. 
                      If you've already installed it, uninstall immediately and scan your device for malware.
                      Only download apps from verified developers.
                    </>
                  ) : (
                    <>
                      This app appears to be legitimate. However, always verify the developer name, 
                      check reviews, and ensure the package ID matches the official app before installing.
                    </>
                  )}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        )}

        {/* Examples */}
        {!result && !loading && (
          <Box sx={{ mt: 4, p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              <strong>Example URLs you can test:</strong>
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
              • https://play.google.com/store/apps/details?id=com.whatsapp<br />
              • https://play.google.com/store/apps/details?id=com.phonepe.app<br />
              • https://apps.apple.com/app/whatsapp-messenger/id310633997
            </Typography>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default QuickCheck;
