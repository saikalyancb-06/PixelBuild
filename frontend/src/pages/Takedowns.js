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
  Chip,
  Button,
} from '@mui/material';
import { takedownsAPI } from '../services/api';

export default function Takedowns() {
  const [takedowns, setTakedowns] = useState([]);

  useEffect(() => {
    fetchTakedowns();
  }, []);

  const fetchTakedowns = async () => {
    try {
      const response = await takedownsAPI.getAll();
      setTakedowns(response.data);
    } catch (error) {
      console.error('Error fetching takedowns:', error);
    }
  };

  const handleAcknowledge = async (id) => {
    try {
      await takedownsAPI.acknowledge(id);
      fetchTakedowns();
    } catch (error) {
      console.error('Error acknowledging takedown:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'taken_down': return 'success';
      case 'acknowledged': return 'info';
      case 'submitted': return 'warning';
      case 'rejected': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Takedown Requests</Typography>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Detection ID</TableCell>
              <TableCell>Store</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Submitted At</TableCell>
              <TableCell>Time to Takedown (hrs)</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {takedowns.map((takedown) => (
              <TableRow key={takedown.id}>
                <TableCell>{takedown.id}</TableCell>
                <TableCell>{takedown.detection_id}</TableCell>
                <TableCell>
                  <Chip label={takedown.store} size="small" />
                </TableCell>
                <TableCell>
                  <Chip
                    label={takedown.status}
                    color={getStatusColor(takedown.status)}
                  />
                </TableCell>
                <TableCell>
                  {new Date(takedown.submitted_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  {takedown.time_to_takedown || '-'}
                </TableCell>
                <TableCell>
                  {takedown.status === 'submitted' && (
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => handleAcknowledge(takedown.id)}
                    >
                      Acknowledge
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
