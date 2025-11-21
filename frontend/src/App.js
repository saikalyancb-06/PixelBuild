import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './pages/Dashboard';
import QuickCheck from './pages/QuickCheck';
import Detections from './pages/Detections';
import Brands from './pages/Brands';
import Scans from './pages/Scans';
import Takedowns from './pages/Takedowns';
import ThreatModel from './pages/ThreatModel';
import MetricsAnalysis from './pages/MetricsAnalysis';
import EvidenceKitGenerator from './pages/EvidenceKitGenerator';
import DetectionPipeline from './pages/DetectionPipeline';
import Layout from './components/Layout';
import { NotificationProvider } from './components/NotificationContext';

const theme = createTheme({
  palette: {
    primary: {
      main: '#667eea',
      dark: '#5568d3',
      light: '#8b9ff5',
    },
    secondary: {
      main: '#764ba2',
      dark: '#5d3c81',
      light: '#9567c4',
    },
    error: {
      main: '#f44336',
    },
    warning: {
      main: '#ff9800',
    },
    success: {
      main: '#4caf50',
    },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 700,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0px 2px 4px rgba(0,0,0,0.05)',
    '0px 4px 8px rgba(0,0,0,0.08)',
    '0px 8px 16px rgba(0,0,0,0.1)',
    '0px 12px 24px rgba(0,0,0,0.12)',
    '0px 16px 32px rgba(0,0,0,0.14)',
    '0px 20px 40px rgba(0,0,0,0.16)',
    '0px 24px 48px rgba(0,0,0,0.18)',
    ...Array(17).fill('0px 24px 48px rgba(0,0,0,0.18)')
  ],
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NotificationProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/quick-check" element={<QuickCheck />} />
              <Route path="/detections" element={<Detections />} />
              <Route path="/brands" element={<Brands />} />
              <Route path="/scans" element={<Scans />} />
              <Route path="/takedowns" element={<Takedowns />} />
              <Route path="/threat-model" element={<ThreatModel />} />
              <Route path="/metrics-analysis" element={<MetricsAnalysis />} />
              <Route path="/evidence-kit" element={<EvidenceKitGenerator />} />
              <Route path="/detection-pipeline" element={<DetectionPipeline />} />
            </Routes>
          </Layout>
        </Router>
      </NotificationProvider>
    </ThemeProvider>
  );
}

export default App;
