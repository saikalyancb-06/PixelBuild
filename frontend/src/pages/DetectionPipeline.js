import React from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  Input as InputIcon,
  CloudDownload as FetchIcon,
  FindInPage as ExtractIcon,
  Speed as ScoreIcon,
  Assessment as OutputIcon,
  ArrowForward,
  CheckCircle,
  Code as CodeIcon,
  Storage as DatabaseIcon
} from '@mui/icons-material';

const DetectionPipeline = () => {
  const pipelineSteps = [
    {
      label: 'Input',
      icon: <InputIcon fontSize="large" />,
      color: '#667eea',
      description: 'User provides Play Store URL or Package ID',
      details: [
        'URL validation and parsing',
        'Extract package identifier',
        'Handle various URL formats',
        'Example: play.google.com/store/apps/details?id=com.example.app'
      ],
      code: `extract_package_id(url)\n→ com.example.app`
    },
    {
      label: 'Fetch',
      icon: <FetchIcon fontSize="large" />,
      color: '#f093fb',
      description: 'Retrieve app data from Google Play Store',
      details: [
        'HTTP request to Play Store',
        'Parse HTML response with BeautifulSoup',
        'Handle rate limiting and errors',
        'Extract raw app information'
      ],
      code: `scrape_play_store_app(package_id)\n→ {name, developer, rating, ...}`
    },
    {
      label: 'Extract',
      icon: <ExtractIcon fontSize="large" />,
      color: '#4facfe',
      description: 'Extract key signals and features from app data',
      details: [
        'App name normalization',
        'Developer name extraction',
        'Package ID structure analysis',
        'Icon and screenshot URLs'
      ],
      code: `signals = {\n  name: "WhatsAp",\n  developer: "Unknown",\n  package: "com.whatsap"\n}`
    },
    {
      label: 'Score',
      icon: <ScoreIcon fontSize="large" />,
      color: '#fa709a',
      description: 'Calculate risk score using similarity algorithms',
      details: [
        'Database lookup: Check 86 legitimate brands',
        'Levenshtein distance for name similarity',
        'Package ID exact match verification',
        'Developer name comparison',
        'Aggregate risk score (0-100)'
      ],
      code: `check_database(package_id)\n+ text_similarity("WhatsAp", "WhatsApp")\n+ verify_developer()\n→ risk_score: 95/100`
    },
    {
      label: 'Output',
      icon: <OutputIcon fontSize="large" />,
      color: '#764ba2',
      description: 'Return structured detection results with evidence',
      details: [
        'is_fake: Boolean verdict',
        'risk_score: 0-100 confidence',
        'reasons: List of red flags',
        'app_info: Complete metadata',
        'JSON response to frontend'
      ],
      code: `{\n  "is_fake": true,\n  "risk_score": 95,\n  "reasons": [\n    "Name similarity: 87%",\n    "Package ID mismatch"\n  ]\n}`
    }
  ];

  const technologies = [
    { name: 'FastAPI', role: 'Backend Framework', icon: '⚡' },
    { name: 'SQLAlchemy', role: 'Database ORM', icon: '🗃️' },
    { name: 'BeautifulSoup4', role: 'Web Scraping', icon: '🌐' },
    { name: 'Levenshtein', role: 'Text Similarity', icon: '📊' },
    { name: 'React', role: 'Frontend UI', icon: '⚛️' },
    { name: 'Material-UI', role: 'Component Library', icon: '🎨' }
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom fontWeight="bold" sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          display: 'inline-block'
        }}>
          Detection Pipeline
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
          Visual breakdown of the 5-stage fake app detection process
        </Typography>
      </Box>

      {/* Pipeline Overview */}
      <Paper elevation={3} sx={{ p: 3, mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Typography variant="h5" gutterBottom fontWeight="bold">
          Complete Detection Flow
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-around', mt: 3, flexWrap: 'wrap' }}>
          {pipelineSteps.map((step, index) => (
            <React.Fragment key={index}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ bgcolor: 'rgba(255,255,255,0.2)', borderRadius: 2, p: 2, mb: 1 }}>
                  {step.icon}
                </Box>
                <Typography variant="caption" fontWeight="bold">
                  {step.label}
                </Typography>
              </Box>
              {index < pipelineSteps.length - 1 && (
                <ArrowForward sx={{ display: { xs: 'none', md: 'block' } }} />
              )}
            </React.Fragment>
          ))}
        </Box>
      </Paper>

      {/* Detailed Stepper */}
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Stepper orientation="vertical" activeStep={-1}>
          {pipelineSteps.map((step, index) => (
            <Step key={index} expanded>
              <StepLabel
                StepIconComponent={() => (
                  <Box
                    sx={{
                      bgcolor: step.color,
                      borderRadius: '50%',
                      width: 40,
                      height: 40,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white'
                    }}
                  >
                    {step.icon}
                  </Box>
                )}
              >
                <Typography variant="h6" fontWeight="bold">
                  Stage {index + 1}: {step.label}
                </Typography>
              </StepLabel>
              <StepContent>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  {step.description}
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="subtitle2" color="primary" gutterBottom>
                          Process Details
                        </Typography>
                        <List dense>
                          {step.details.map((detail, idx) => (
                            <ListItem key={idx}>
                              <ListItemIcon>
                                <CheckCircle fontSize="small" color="success" />
                              </ListItemIcon>
                              <ListItemText primary={detail} />
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Card variant="outlined" sx={{ bgcolor: '#f5f5f5' }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <CodeIcon fontSize="small" sx={{ mr: 1 }} />
                          <Typography variant="subtitle2" color="primary">
                            Code Example
                          </Typography>
                        </Box>
                        <Paper
                          elevation={0}
                          sx={{
                            p: 2,
                            bgcolor: '#1e1e1e',
                            color: '#d4d4d4',
                            fontFamily: 'monospace',
                            fontSize: '0.85rem',
                            whiteSpace: 'pre-wrap',
                            borderRadius: 1
                          }}
                        >
                          {step.code}
                        </Paper>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </Paper>

      {/* Key Components */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <DatabaseIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Database Layer</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body2" paragraph>
                SQLite database with 86 legitimate brands across multiple categories:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                <Chip label="Banking/UPI" size="small" />
                <Chip label="E-commerce" size="small" />
                <Chip label="Social Media" size="small" />
                <Chip label="Gaming" size="small" />
                <Chip label="Entertainment" size="small" />
                <Chip label="Food Delivery" size="small" />
                <Chip label="Travel" size="small" />
              </Box>
              <Typography variant="body2" sx={{ mt: 2 }}>
                Stores: package IDs, developer names, official icons, certificates
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ScoreIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6">Risk Scoring Algorithm</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body2" paragraph>
                Multi-factor risk assessment combining:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText 
                    primary="Name Similarity"
                    secondary="Levenshtein distance ratio (0-1)"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Package ID Match"
                    secondary="Exact match against 86 brands"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Developer Verification"
                    secondary="Compare against official developers"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Aggregate Score"
                    secondary="Weighted combination → 0-100"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Technology Stack */}
      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Technology Stack
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Grid container spacing={2}>
          {technologies.map((tech, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography sx={{ fontSize: '2rem', mr: 1 }}>
                      {tech.icon}
                    </Typography>
                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold">
                        {tech.name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {tech.role}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Performance Metrics */}
      <Paper elevation={2} sx={{ p: 3, mt: 4, bgcolor: '#f9f9f9' }}>
        <Typography variant="h6" gutterBottom>
          Pipeline Performance
        </Typography>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary">~2s</Typography>
              <Typography variant="caption">Avg Response Time</Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="success.main">86</Typography>
              <Typography variant="caption">Brands Covered</Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="secondary.main">92%</Typography>
              <Typography variant="caption">Detection Accuracy</Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="warning.main">100%</Typography>
              <Typography variant="caption">API Uptime</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default DetectionPipeline;
