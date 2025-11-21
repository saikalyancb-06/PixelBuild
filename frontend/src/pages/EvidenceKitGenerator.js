import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Alert,
  CircularProgress,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Description as DescriptionIcon,
  GetApp as DownloadIcon,
  Email as EmailIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  ContentCopy as CopyIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

const EvidenceKitGenerator = () => {
  const [detectionId, setDetectionId] = useState('');
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [evidenceKit, setEvidenceKit] = useState(null);
  const [error, setError] = useState('');
  const [showEmail, setShowEmail] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);

  useEffect(() => {
    fetchRecentDetections();
  }, []);

  const fetchRecentDetections = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/detections');
      setDetections(response.data.slice(0, 10)); // Last 10 detections
    } catch (err) {
      console.error('Error fetching detections:', err);
    }
  };

  const generateEvidenceKit = async () => {
    if (!detectionId) {
      setError('Please enter a detection ID');
      return;
    }

    setLoading(true);
    setError('');
    setEvidenceKit(null);

    try {
      const response = await axios.post('http://localhost:8000/api/evidence-kit/generate', {
        detection_id: parseInt(detectionId)
      });
      setEvidenceKit(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate evidence kit');
    } finally {
      setLoading(false);
    }
  };

  const downloadJSON = () => {
    if (!evidenceKit) return;

    const blob = new Blob([JSON.stringify(evidenceKit, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evidence_kit_${detectionId}_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyEmailToClipboard = () => {
    if (!evidenceKit) return;

    navigator.clipboard.writeText(evidenceKit.takedown_email).then(() => {
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    });
  };

  const renderEvidenceKit = () => {
    if (!evidenceKit) return null;

    return (
      <Box sx={{ mt: 4 }}>
        {/* Header */}
        <Paper elevation={3} sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
          <Grid container alignItems="center" spacing={2}>
            <Grid item>
              <SecurityIcon sx={{ fontSize: 48 }} />
            </Grid>
            <Grid item xs>
              <Typography variant="h5" fontWeight="bold">
                Evidence Kit Generated
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                Detection ID: {evidenceKit.detection_id} • Generated: {new Date(evidenceKit.generated_at).toLocaleString()}
              </Typography>
            </Grid>
            <Grid item>
              <Chip
                label={`Risk: ${evidenceKit.risk_score}%`}
                color={evidenceKit.risk_score > 70 ? 'error' : 'warning'}
                sx={{ fontWeight: 'bold', fontSize: '1rem', height: 40 }}
              />
            </Grid>
          </Grid>
        </Paper>

        {/* App Information */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <WarningIcon color="error" sx={{ mr: 1 }} />
                  <Typography variant="h6">Suspicious App</Typography>
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ display: 'flex', mb: 2 }}>
                  {(evidenceKit.evidence.evidence_attachments.app_icon_base64 || evidenceKit.evidence.app_information.icon_url) && (
                    <img 
                      src={evidenceKit.evidence.evidence_attachments.app_icon_base64 
                        ? `data:image/png;base64,${evidenceKit.evidence.evidence_attachments.app_icon_base64}` 
                        : evidenceKit.evidence.app_information.icon_url
                      }
                      alt="App icon" 
                      style={{ width: 80, height: 80, borderRadius: 8, marginRight: 16, objectFit: 'cover' }}
                    />
                  )}
                  <Box>
                    <Typography variant="h6" color="error.main">{evidenceKit.app_name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {evidenceKit.evidence.app_information.developer_name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Installs: {evidenceKit.evidence.app_information.install_count}
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" sx={{ wordBreak: 'break-all', bgcolor: '#f5f5f5', p: 1, borderRadius: 1 }}>
                  <strong>Package ID:</strong> {evidenceKit.package_id}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <CheckIcon color="success" sx={{ mr: 1 }} />
                  <Typography variant="h6">Legitimate Brand</Typography>
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ display: 'flex', mb: 2 }}>
                  {(evidenceKit.evidence.evidence_attachments.official_icon_base64 || evidenceKit.evidence.legitimate_brand.official_icon_urls) && (
                    <img 
                      src={evidenceKit.evidence.evidence_attachments.official_icon_base64 
                        ? `data:image/png;base64,${evidenceKit.evidence.evidence_attachments.official_icon_base64}` 
                        : evidenceKit.evidence.legitimate_brand.official_icon_urls[0]
                      }
                      alt="Brand icon" 
                      style={{ width: 80, height: 80, borderRadius: 8, marginRight: 16, objectFit: 'cover' }}
                    />
                  )}
                  <Box>
                    <Typography variant="h6" color="success.main">{evidenceKit.brand_name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {evidenceKit.evidence.legitimate_brand.official_developer}
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" sx={{ wordBreak: 'break-all', bgcolor: '#f5f5f5', p: 1, borderRadius: 1 }}>
                  <strong>Official Package(s):</strong><br />
                  {Array.isArray(evidenceKit.evidence.legitimate_brand.official_package_ids) 
                    ? evidenceKit.evidence.legitimate_brand.official_package_ids.join(', ')
                    : evidenceKit.evidence.legitimate_brand.official_package_ids}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Similarity Scores */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Similarity Analysis</Typography>
                <Divider sx={{ mb: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={6} sm={3}>
                    <Paper elevation={0} sx={{ p: 2, bgcolor: '#fff3e0', textAlign: 'center' }}>
                      <Typography variant="h4" color="warning.main">
                        {Math.round(evidenceKit.evidence.similarity_scores.name_similarity * 100)}%
                      </Typography>
                      <Typography variant="caption">Name Similarity</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Paper elevation={0} sx={{ p: 2, bgcolor: '#fce4ec', textAlign: 'center' }}>
                      <Typography variant="h4" color="error.main">
                        {Math.round(evidenceKit.evidence.similarity_scores.icon_similarity * 100)}%
                      </Typography>
                      <Typography variant="caption">Icon Similarity</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Paper elevation={0} sx={{ p: 2, bgcolor: '#e8eaf6', textAlign: 'center' }}>
                      <Typography variant="h4" color="primary.main">
                        {Math.round(evidenceKit.evidence.similarity_scores.package_similarity * 100)}%
                      </Typography>
                      <Typography variant="caption">Package Similarity</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Paper elevation={0} sx={{ p: 2, bgcolor: '#ffebee', textAlign: 'center' }}>
                      <Typography variant="h4" color="error.main" fontWeight="bold">
                        {Math.round(evidenceKit.evidence.similarity_scores.overall_risk_score * 100)}%
                      </Typography>
                      <Typography variant="caption">Overall Risk</Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Red Flags */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom color="error">Red Flags Identified</Typography>
                <Divider sx={{ mb: 2 }} />
                <List>
                  {evidenceKit.evidence.red_flags.map((flag, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <WarningIcon color="error" />
                      </ListItemIcon>
                      <ListItemText primary={flag} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Action Buttons */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3, bgcolor: '#f5f5f5' }}>
              <Typography variant="h6" gutterBottom>Export Evidence</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<DownloadIcon />}
                    onClick={downloadJSON}
                    sx={{ py: 1.5 }}
                  >
                    Download JSON
                  </Button>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Button
                    fullWidth
                    variant="contained"
                    color="secondary"
                    startIcon={<EmailIcon />}
                    onClick={() => setShowEmail(true)}
                    sx={{ py: 1.5 }}
                  >
                    View Takedown Email
                  </Button>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<InfoIcon />}
                    href={evidenceKit.evidence.app_information.store_url}
                    target="_blank"
                    sx={{ py: 1.5 }}
                  >
                    Open Store Page
                  </Button>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        </Grid>

        {/* Email Dialog */}
        <Dialog open={showEmail} onClose={() => setShowEmail(false)} maxWidth="md" fullWidth>
          <DialogTitle>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <EmailIcon sx={{ mr: 1 }} />
                Takedown Request Email Template
              </Box>
              <Tooltip title={copySuccess ? "Copied!" : "Copy to clipboard"}>
                <IconButton onClick={copyEmailToClipboard} color={copySuccess ? "success" : "default"}>
                  <CopyIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </DialogTitle>
          <DialogContent dividers>
            <TextField
              multiline
              fullWidth
              rows={20}
              value={evidenceKit.takedown_email}
              InputProps={{
                readOnly: true,
                style: { fontFamily: 'monospace', fontSize: '0.9rem' }
              }}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowEmail(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      </Box>
    );
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom fontWeight="bold" sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          display: 'inline-block'
        }}>
          Evidence Kit Generator
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
          Generate comprehensive evidence packages for flagged apps, including similarity analysis and takedown request templates
        </Typography>
      </Box>

      {/* Input Section */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={8}>
            <TextField
              fullWidth
              label="Detection ID"
              variant="outlined"
              value={detectionId}
              onChange={(e) => setDetectionId(e.target.value)}
              placeholder="Enter detection ID to generate evidence kit"
              type="number"
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button
              fullWidth
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <DescriptionIcon />}
              onClick={generateEvidenceKit}
              disabled={loading}
              sx={{ py: 1.5 }}
            >
              {loading ? 'Generating...' : 'Generate Kit'}
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {/* Recent Detections Helper */}
      {detections.length > 0 && !evidenceKit && (
        <Paper elevation={1} sx={{ p: 2, mb: 3, bgcolor: '#f9f9f9' }}>
          <Typography variant="subtitle2" gutterBottom>
            Recent Detections (Click to select):
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {detections.map((detection) => (
              <Chip
                key={detection.id}
                label={`ID: ${detection.id} - ${detection.suspicious_app?.app_name || 'Unknown'}`}
                onClick={() => setDetectionId(detection.id.toString())}
                variant={detectionId === detection.id.toString() ? 'filled' : 'outlined'}
                color={detectionId === detection.id.toString() ? 'primary' : 'default'}
              />
            ))}
          </Box>
        </Paper>
      )}

      {/* Evidence Kit Display */}
      {renderEvidenceKit()}
    </Container>
  );
};

export default EvidenceKitGenerator;
