import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const brandsAPI = {
  getAll: () => api.get('/brands'),
  getById: (id) => api.get(`/brands/${id}`),
  create: (data) => api.post('/brands', data),
};

export const scansAPI = {
  getAll: () => api.get('/scans'),
  getById: (id) => api.get(`/scans/${id}`),
  create: (data) => api.post('/scans', data),
};

export const detectionsAPI = {
  getAll: (params) => api.get('/detections', { params }),
  getById: (id) => api.get(`/detections/${id}`),
  confirm: (id) => api.post(`/detections/${id}/confirm`),
  markFalsePositive: (id) => api.post(`/detections/${id}/false-positive`),
};

export const takedownsAPI = {
  getAll: () => api.get('/takedowns'),
  getById: (id) => api.get(`/takedowns/${id}`),
  create: (data) => api.post('/takedowns', data),
  acknowledge: (id) => api.post(`/takedowns/${id}/acknowledge`),
};

export const metricsAPI = {
  getOverall: () => api.get('/metrics'),
  getDashboard: () => api.get('/metrics/dashboard'),
};

export default api;
