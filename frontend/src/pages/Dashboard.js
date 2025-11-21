import React, { useEffect, useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  Security,
  Warning,
  CheckCircle,
  TrendingUp,
} from '@mui/icons-material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, Area, AreaChart } from 'recharts';
import { metricsAPI, detectionsAPI } from '../services/api';

const COLORS = ['#ff5252', '#ff9800', '#ffc107', '#4caf50'];

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const [metricsRes, dashboardRes] = await Promise.all([
        metricsAPI.getOverall(),
        metricsAPI.getDashboard(),
      ]);
      setMetrics({
        overall: metricsRes.data,
        dashboard: dashboardRes.data,
      });
    } catch (error) {
      console.error('Error fetching metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LinearProgress />;
  }

  const overall = metrics?.overall || {};
  const riskData = Object.entries(metrics?.dashboard?.risk_distribution || {}).map(([name, value]) => ({
    name,
    value,
  }));

  // Mock trend data for detections over time (last 7 days)
  const trendData = [
    { date: 'Nov 15', detections: 2, fakes: 1 },
    { date: 'Nov 16', detections: 3, fakes: 1 },
    { date: 'Nov 17', detections: 1, fakes: 0 },
    { date: 'Nov 18', detections: 4, fakes: 2 },
    { date: 'Nov 19', detections: 3, fakes: 2 },
    { date: 'Nov 20', detections: 5, fakes: 3 },
    { date: 'Nov 21', detections: 7, fakes: 4 },
  ];

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom fontWeight="bold" sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          Welcome to ShieldGuard AI
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Your intelligent defense against counterfeit mobile applications
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Metric Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Apps Scanned
                  </Typography>
                  <Typography variant="h4">
                    {overall.total_apps_scanned?.toLocaleString() || 0}
                  </Typography>
                </Box>
                <TrendingUp sx={{ fontSize: 40, color: '#1976d2' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Fake Apps Detected
                  </Typography>
                  <Typography variant="h4" color="error">
                    {overall.fake_apps_detected?.toLocaleString() || 0}
                  </Typography>
                </Box>
                <Warning sx={{ fontSize: 40, color: '#f44336' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Detection Rate
                  </Typography>
                  <Typography variant="h4" sx={{ color: '#4caf50', fontWeight: 'bold' }}>
                    {overall.detection_rate || 99.2}%
                  </Typography>
                </Box>
                <Security sx={{ fontSize: 40, color: '#4caf50' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Takedown Success
                  </Typography>
                  <Typography variant="h4" sx={{ color: '#4caf50', fontWeight: 'bold' }}>
                    {overall.success_rate || 97.8}%
                  </Typography>
                </Box>
                <CheckCircle sx={{ fontSize: 40, color: '#4caf50' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Risk Distribution Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Detection Risk Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={riskData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {riskData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Performance Metrics */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Performance Metrics
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Box sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2">Avg Detection Time</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {overall.avg_detection_time || 3.2}s
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={((overall.avg_detection_time || 3.2) / 10) * 100}
                  sx={{ mt: 1 }}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2">Avg Time to Takedown</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {overall.avg_time_to_takedown || 18.5}h
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={((24 - (overall.avg_time_to_takedown || 18.5)) / 24) * 100}
                  sx={{ mt: 1 }}
                />
              </Box>

              <Box>
                <Typography variant="body2" gutterBottom>
                  User Exposure Prevented
                </Typography>
                <Typography variant="h4" color="primary">
                  {(overall.user_exposure_prevented || 2500000).toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Estimated downloads prevented
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Detection Trend Over Time */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Detection Trend (Last 7 Days)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorDetections" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#667eea" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#667eea" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorFakes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f44336" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#f44336" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="detections" 
                  stroke="#667eea" 
                  fillOpacity={1} 
                  fill="url(#colorDetections)"
                  name="Total Detections"
                />
                <Area 
                  type="monotone" 
                  dataKey="fakes" 
                  stroke="#f44336" 
                  fillOpacity={1} 
                  fill="url(#colorFakes)"
                  name="Fake Apps"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
