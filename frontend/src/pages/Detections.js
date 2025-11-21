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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import { Warning, CheckCircle, Error } from '@mui/icons-material';
import { detectionsAPI, takedownsAPI } from '../services/api';

const getRiskColor = (risk) => {
  switch (risk) {
    case 'CRITICAL': return 'error';
    case 'HIGH': return 'error';
    case 'MEDIUM': return 'warning';
    case 'LOW': return 'success';
    default: return 'default';
  }
};

export default function Detections() {
  const [detections, setDetections] = useState([]);
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [minConfidence, setMinConfidence] = useState(0.7);

  useEffect(() => {
    fetchDetections();
  }, [minConfidence]);

  const fetchDetections = async () => {
    try {
      const response = await detectionsAPI.getAll({ min_confidence: minConfidence });
      setDetections(response.data);
    } catch (error) {
      console.error('Error fetching detections:', error);
    }
  };

  const handleCreateTakedown = async (detectionId) => {
    try {
      await takedownsAPI.create({
        detection_id: detectionId,
        store: 'play_store',
      });
      alert('Takedown request created successfully!');
      fetchDetections();
    } catch (error) {
      console.error('Error creating takedown:', error);
      alert('Failed to create takedown request');
    }
  };

  const handleConfirm = async (detectionId) => {
    try {
      await detectionsAPI.confirm(detectionId);
      fetchDetections();
    } catch (error) {
      console.error('Error confirming detection:', error);
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Detections</Typography>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Min Confidence</InputLabel>
          <Select
            value={minConfidence}
            onChange={(e) => setMinConfidence(e.target.value)}
            label="Min Confidence"
          >
            <MenuItem value={0.5}>50%</MenuItem>
            <MenuItem value={0.7}>70%</MenuItem>
            <MenuItem value={0.8}>80%</MenuItem>
            <MenuItem value={0.9}>90%</MenuItem>
            <MenuItem value={0.95}>95%</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Brand</TableCell>
              <TableCell>Confidence</TableCell>
              <TableCell>Risk Level</TableCell>
              <TableCell>Icon Similarity</TableCell>
              <TableCell>Text Similarity</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Detected At</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {detections.map((detection) => (
              <TableRow key={detection.id}>
                <TableCell>{detection.id}</TableCell>
                <TableCell>{detection.brand_id}</TableCell>
                <TableCell>
                  <strong>{(detection.confidence_score * 100).toFixed(1)}%</strong>
                </TableCell>
                <TableCell>
                  <Chip
                    label={detection.risk_level}
                    color={getRiskColor(detection.risk_level)}
                    icon={detection.risk_level === 'CRITICAL' ? <Error /> : <Warning />}
                  />
                </TableCell>
                <TableCell>{(detection.icon_similarity_score * 100).toFixed(1)}%</TableCell>
                <TableCell>{(detection.text_similarity_score * 100).toFixed(1)}%</TableCell>
                <TableCell>
                  <Chip
                    label={detection.status}
                    color={detection.status === 'confirmed' ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {new Date(detection.detected_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => {
                      setSelectedDetection(detection);
                      setOpenDialog(true);
                    }}
                  >
                    View
                  </Button>
                  {detection.status === 'pending' && (
                    <>
                      <Button
                        size="small"
                        color="success"
                        onClick={() => handleConfirm(detection.id)}
                        sx={{ ml: 1 }}
                      >
                        Confirm
                      </Button>
                      <Button
                        size="small"
                        color="error"
                        onClick={() => handleCreateTakedown(detection.id)}
                        sx={{ ml: 1 }}
                      >
                        Takedown
                      </Button>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Detection Details</DialogTitle>
        <DialogContent>
          {selectedDetection && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Risk Level: {selectedDetection.risk_level}
              </Typography>
              <Typography variant="body1" paragraph>
                Confidence Score: {(selectedDetection.confidence_score * 100).toFixed(2)}%
              </Typography>
              <Typography variant="h6" gutterBottom>
                Detection Reasons:
              </Typography>
              <ul>
                {selectedDetection.detection_reasons?.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
