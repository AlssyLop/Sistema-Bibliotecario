import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Variables to handle loading spinner
let activeRequests = 0;
let showLoading = null;
let hideLoading = null;

export const setLoadingCallbacks = (show, hide) => {
  showLoading = show;
  hideLoading = hide;
};

api.interceptors.request.use((config) => {
  if (activeRequests === 0 && showLoading) {
    showLoading();
  }
  activeRequests++;
  return config;
}, (error) => {
  activeRequests--;
  if (activeRequests === 0 && hideLoading) {
    hideLoading();
  }
  return Promise.reject(error);
});

api.interceptors.response.use((response) => {
  activeRequests--;
  if (activeRequests === 0 && hideLoading) {
    hideLoading();
  }
  return response;
}, (error) => {
  activeRequests--;
  if (activeRequests === 0 && hideLoading) {
    hideLoading();
  }
  return Promise.reject(error);
});

export default api;
