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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { brandsAPI } from '../services/api';

export default function Brands() {
  const [brands, setBrands] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [newBrand, setNewBrand] = useState({
    name: '',
    developer_name: '',
    package_ids: '',
    icon_urls: '',
  });

  useEffect(() => {
    fetchBrands();
  }, []);

  const fetchBrands = async () => {
    try {
      const response = await brandsAPI.getAll();
      setBrands(response.data);
    } catch (error) {
      console.error('Error fetching brands:', error);
    }
  };

  const handleCreateBrand = async () => {
    try {
      await brandsAPI.create({
        name: newBrand.name,
        developer_name: newBrand.developer_name,
        package_ids: newBrand.package_ids.split(',').map(s => s.trim()),
        icon_urls: newBrand.icon_urls.split(',').map(s => s.trim()),
        certificates: [],
      });
      setOpenDialog(false);
      fetchBrands();
      setNewBrand({ name: '', developer_name: '', package_ids: '', icon_urls: '' });
    } catch (error) {
      console.error('Error creating brand:', error);
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Protected Brands</Typography>
        <Button variant="contained" onClick={() => setOpenDialog(true)}>
          Add Brand
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Brand Name</TableCell>
              <TableCell>Developer</TableCell>
              <TableCell>Package IDs</TableCell>
              <TableCell>Created At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {brands.map((brand) => (
              <TableRow key={brand.id}>
                <TableCell>{brand.id}</TableCell>
                <TableCell>{brand.name}</TableCell>
                <TableCell>{brand.developer_name}</TableCell>
                <TableCell>{brand.package_ids?.join(', ')}</TableCell>
                <TableCell>
                  {new Date(brand.created_at).toLocaleDateString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Add New Brand</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Brand Name"
            fullWidth
            value={newBrand.name}
            onChange={(e) => setNewBrand({ ...newBrand, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Developer Name"
            fullWidth
            value={newBrand.developer_name}
            onChange={(e) => setNewBrand({ ...newBrand, developer_name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Package IDs (comma-separated)"
            fullWidth
            value={newBrand.package_ids}
            onChange={(e) => setNewBrand({ ...newBrand, package_ids: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Icon URLs (comma-separated)"
            fullWidth
            value={newBrand.icon_urls}
            onChange={(e) => setNewBrand({ ...newBrand, icon_urls: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateBrand} variant="contained">
            Add Brand
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
