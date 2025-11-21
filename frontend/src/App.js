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
import Layout from './components/Layout';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/quick-check" element={<QuickCheck />} />
            <Route path="/detections" element={<Detections />} />
            <Route path="/brands" element={<Brands />} />
            <Route path="/scans" element={<Scans />} />
            <Route path="/takedowns" element={<Takedowns />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
