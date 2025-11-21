import React from 'react';
import {
  Container, Typography, Paper, Box, Grid,
  Card, CardContent
} from '@mui/material';
import {
  Warning, Person, Security, Block
} from '@mui/icons-material';
import '../styles/ThreatModelUniform.css';

function ThreatModel() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Threat Model & System Analysis
      </Typography>

      <Grid container spacing={3} className="threat-model-grid">
        {/* Uniform Card Grid */}
        {[{
          icon: <Person color="error" sx={{ mr: 1, fontSize: 40 }} />, title: 'Who is the Attacker?',
          content: <>
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
          </>
        }, {
          icon: <Warning color="warning" sx={{ mr: 1, fontSize: 40 }} />, title: 'Who are the Victims?',
          content: <>
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
          </>
        }, {
          icon: <Security color="success" sx={{ mr: 1, fontSize: 40 }} />, title: 'What Does Our System Cover?',
          content: <>
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
          </>
        }, {
          icon: <Block color="error" sx={{ mr: 1, fontSize: 40 }} />, title: `What We Don't Cover`,
          content: <>
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
          </>
        }].map((card, idx) => (
          <Grid item xs={12} sm={6} md={3} key={idx} className="threat-model-card-grid-item">
            <Card className="threat-model-card" elevation={4}>
              <CardContent className="threat-model-card-content">
                <Box display="flex" alignItems="center" mb={2}>
                  {card.icon}
                  <Typography variant="h6">{card.title}</Typography>
                </Box>
                {card.content}
              </CardContent>
            </Card>
          </Grid>
        ))}

        {/* Ethics & Legal */}
        <Grid item xs={12} className="threat-model-ethics-grid-item">
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
