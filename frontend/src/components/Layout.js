import React from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Security as SecurityIcon,
  BusinessCenter as BrandsIcon,
  Search as SearchIcon,
  Report as ReportIcon,
  Assessment as AssessmentIcon,
  Policy as PolicyIcon,
  Description as DescriptionIcon,
  AccountTree as PipelineIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Quick Check', icon: <SearchIcon />, path: '/quick-check' },
  { text: 'Detections', icon: <SecurityIcon />, path: '/detections' },
  { text: 'Brands', icon: <BrandsIcon />, path: '/brands' },
  { text: 'Scans', icon: <SearchIcon />, path: '/scans' },
  { text: 'Takedowns', icon: <ReportIcon />, path: '/takedowns' },
  { text: 'divider', isDivider: true },
  { text: 'Threat Model', icon: <PolicyIcon />, path: '/threat-model' },
  { text: 'Metrics Analysis', icon: <AssessmentIcon />, path: '/metrics-analysis' },
  { text: 'Evidence Kit', icon: <DescriptionIcon />, path: '/evidence-kit' },
  { text: 'Detection Pipeline', icon: <PipelineIcon />, path: '/detection-pipeline' },
];

export default function Layout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{ 
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}
      >
        <Toolbar>
          <SecurityIcon sx={{ mr: 2, fontSize: 32 }} />
          <Box>
            <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 'bold', letterSpacing: 1 }}>
              ShieldGuard AI
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.9 }}>
              Advanced Fake App Detection
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item, index) => (
              item.isDivider ? (
                <Divider key={index} sx={{ my: 1 }} />
              ) : (
                <ListItem key={item.text} disablePadding>
                  <ListItemButton
                    selected={location.pathname === item.path}
                    onClick={() => navigate(item.path)}
                  >
                    <ListItemIcon>{item.icon}</ListItemIcon>
                    <ListItemText primary={item.text} />
                  </ListItemButton>
                </ListItem>
              )
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}
