import api from '../../services/httpInterceptor';

export const getBooks = async () => {
  const response = await api.get('/libros');
  return response.data;
};

export const createBook = async (data) => {
  const response = await api.post('/libros', data);
  return response.data;
};

export const updateBook = async (id, data) => {
  const response = await api.put(`/libros/${id}`, data);
  return response.data;
};

export const deleteBook = async (id) => {
  const response = await api.delete(`/libros/${id}`);
  return response.data;
};
