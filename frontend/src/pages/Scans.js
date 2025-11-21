import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
} from '@mui/material';
import { scansAPI, brandsAPI } from '../services/api';

export default function Scans() {
  const [scans, setScans] = useState([]);
  const [brands, setBrands] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedBrand, setSelectedBrand] = useState('');
  const [sources, setSources] = useState(['play_store', 'apk_mirror']);

  useEffect(() => {
    fetchScans();
    fetchBrands();
  }, []);

  const fetchScans = async () => {
    try {
      const response = await scansAPI.getAll();
      setScans(response.data);
    } catch (error) {
      console.error('Error fetching scans:', error);
    }
  };

  const fetchBrands = async () => {
    try {
      const response = await brandsAPI.getAll();
      setBrands(response.data);
    } catch (error) {
      console.error('Error fetching brands:', error);
    }
  };

  const handleCreateScan = async () => {
    try {
      await scansAPI.create({
        brand_id: selectedBrand,
        sources: sources,
      });
      setOpenDialog(false);
      fetchScans();
      setSelectedBrand('');
    } catch (error) {
      console.error('Error creating scan:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'running': return 'info';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Scan Jobs</Typography>
        <Button variant="contained" onClick={() => setOpenDialog(true)}>
          New Scan
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Brand ID</TableCell>
              <TableCell>Sources</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Apps Scanned</TableCell>
              <TableCell>Detections</TableCell>
              <TableCell>Created At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {scans.map((scan) => (
              <TableRow key={scan.id}>
                <TableCell>{scan.id}</TableCell>
                <TableCell>{scan.brand_id}</TableCell>
                <TableCell>{scan.sources?.join(', ')}</TableCell>
                <TableCell>
                  <Chip
                    label={scan.status}
                    color={getStatusColor(scan.status)}
                    icon={scan.status === 'running' ? <CircularProgress size={16} /> : null}
                  />
                </TableCell>
                <TableCell>{scan.apps_scanned}</TableCell>
                <TableCell>
                  <Chip
                    label={scan.detections_found}
                    color={scan.detections_found > 0 ? 'error' : 'default'}
                  />
                </TableCell>
                <TableCell>
                  {new Date(scan.created_at).toLocaleDateString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Create New Scan</DialogTitle>
        <DialogContent sx={{ minWidth: 400 }}>
          <FormControl fullWidth margin="dense">
            <InputLabel>Brand</InputLabel>
            <Select
              value={selectedBrand}
              onChange={(e) => setSelectedBrand(e.target.value)}
              label="Brand"
            >
              {brands.map((brand) => (
                <MenuItem key={brand.id} value={brand.id}>
                  {brand.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel>Sources</InputLabel>
            <Select
              multiple
              value={sources}
              onChange={(e) => setSources(e.target.value)}
              label="Sources"
            >
              <MenuItem value="play_store">Google Play Store</MenuItem>
              <MenuItem value="app_store">Apple App Store</MenuItem>
              <MenuItem value="apk_mirror">APK Mirror</MenuItem>
              <MenuItem value="apk_pure">APK Pure</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateScan} variant="contained" disabled={!selectedBrand}>
            Start Scan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
