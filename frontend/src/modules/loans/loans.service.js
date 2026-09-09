import api from '../../services/httpInterceptor';

export const getActiveLoans = async () => {
  const response = await api.get('/prestamos/activos');
  return response.data;
};

export const getPendingLoans = async () => {
  const response = await api.get('/prestamos/pendientes');
  return response.data;
};

export const createLoan = async (data) => {
  const response = await api.post('/prestamos', data);
  return response.data;
};

export const returnLoan = async (id) => {
  const response = await api.post(`/prestamos/${id}/devolucion`);
  return response.data;
};
