import React, { useState, useEffect } from 'react';
import { BrowserRouter } from 'react-router-dom';
import AppRouter from './routes/AppRouter';
import LoadingSpinner from './components/shared/LoadingSpinner';
import ToastContainer from './components/shared/ToastContainer';
import api, { setLoadingCallbacks } from './services/httpInterceptor';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    setLoadingCallbacks(
      () => setIsLoading(true),
      () => setIsLoading(false)
    );

    // Add response interceptor for global error handling with Toasts
    const errorInterceptor = api.interceptors.response.use(
      (response) => response,
      (error) => {
        const message = error.response?.data?.detail || error.message || 'Error inesperado';
        addToast(message, 'danger');
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.response.eject(errorInterceptor);
    };
  }, []);

  const addToast = (message, type = 'success') => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      removeToast(id);
    }, 5000);
  };

  const removeToast = (id) => {
    setToasts((prev) => prev.filter(t => t.id !== id));
  };

  return (
    <BrowserRouter>
      <AppRouter />
      <LoadingSpinner show={isLoading} />
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </BrowserRouter>
  );
}

export default App;
