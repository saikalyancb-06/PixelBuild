import React from 'react';
import {
  Container, Typography, Paper, Box, Grid,
  Card, CardContent, Alert
} from '@mui/material';
import {
  Warning, Person, Business, Security, Block
} from '@mui/icons-material';

function ThreatModel() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Threat Model & System Analysis
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Academic Prototype Notice:</strong> This is an educational system developed for hackathon purposes. 
        It demonstrates detection concepts and is not a production-ready security solution.
      </Alert>

      <Grid container spacing={3}>
        {/* Attacker Profile */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Person color="error" sx={{ mr: 1, fontSize: 40 }} />
                <Typography variant="h6">Who is the Attacker?</Typography>
              </Box>
              <Typography variant="body2" paragraph>
                <strong>Profile:</strong> Fraudsters, scammers, and malicious actors
              </Typography>
              <Typography variant="body2" component="div">
                <strong>Tactics:</strong>
                <ul>
                  <li>Create fake apps with similar names to legitimate brands</li>
                  <li>Use similar icons and branding to deceive users</li>
                  <li>Publish on Play Store or APK mirror sites</li>
                  <li>Target popular banking, payment, and e-commerce apps</li>
                  <li>Steal credentials, UPI PINs, and financial data</li>
                </ul>
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Victim Profile */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Warning color="warning" sx={{ mr: 1, fontSize: 40 }} />
                <Typography variant="h6">Who are the Victims?</Typography>
              </Box>
              <Typography variant="body2" paragraph>
                <strong>Primary Victims:</strong>
              </Typography>
              <Typography variant="body2" component="div">
                <ul>
                  <li><strong>End Users:</strong> Credential theft, financial loss, identity theft</li>
                  <li><strong>Brands:</strong> Reputational damage, customer trust erosion</li>
                  <li><strong>App Stores:</strong> Platform integrity, user safety concerns</li>
                </ul>
              </Typography>
              <Typography variant="body2" paragraph sx={{ mt: 2 }}>
                <strong>Impact:</strong> Financial fraud, data breaches, chargebacks, legal liabilities
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* System Coverage */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Security color="success" sx={{ mr: 1, fontSize: 40 }} />
                <Typography variant="h6">What Does Our System Cover?</Typography>
              </Box>
              <Typography variant="body2" component="div">
                <strong>Detection Capabilities:</strong>
                <ul>
                  <li>✓ Package ID verification against known legitimate apps</li>
                  <li>✓ Name similarity detection (Levenshtein distance)</li>
                  <li>✓ Real-time Play Store data scraping</li>
                  <li>✓ Developer name matching</li>
                  <li>✓ Multi-signal risk scoring (0-100)</li>
                  <li>✓ 86+ brands database coverage</li>
                </ul>
              </Typography>
              <Typography variant="body2" paragraph sx={{ mt: 2 }}>
                <strong>Scope:</strong> Android Play Store apps, Banking/UPI/E-commerce focus
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Limitations */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Block color="error" sx={{ mr: 1, fontSize: 40 }} />
                <Typography variant="h6">What We Don't Cover</Typography>
              </Box>
              <Typography variant="body2" component="div">
                <strong>Out of Scope:</strong>
                <ul>
                  <li>✗ Overlay malware (installed via side-loading only)</li>
                  <li>✗ Non-store-based phishing (SMS, email, web)</li>
                  <li>✗ iOS App Store apps</li>
                  <li>✗ Deep APK analysis / reverse engineering</li>
                  <li>✗ Runtime behavior monitoring</li>
                  <li>✗ Network traffic analysis</li>
                  <li>✗ Zero-day malware detection</li>
                </ul>
              </Typography>
              <Typography variant="body2" paragraph sx={{ mt: 2 }}>
                <strong>Note:</strong> This is a surface-level detection system focused on impersonation patterns.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Ethics & Legal */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, bgcolor: '#fff3cd' }}>
            <Typography variant="h6" gutterBottom color="text.primary">
              ⚖️ Ethics & Legal Compliance
            </Typography>
            <Typography variant="body2" component="div">
              <strong>Do No Harm Policy:</strong>
              <ul>
                <li>No real malware execution on personal machines</li>
                <li>No abusive scraping or violating store Terms of Service</li>
                <li>No doxxing or naming individuals - only app-level analysis</li>
                <li>Educational and research purposes only</li>
                <li>Not intended for production security deployment</li>
                <li>Users should verify findings independently before taking action</li>
              </ul>
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default ThreatModel;
