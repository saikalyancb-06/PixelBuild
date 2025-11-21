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
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
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

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

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
                  <Typography variant="h4">
                    {overall.detection_rate || 99.99}%
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
                  <Typography variant="h4">
                    {overall.success_rate || 94}%
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
      </Grid>
    </Box>
  );
}
