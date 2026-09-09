import api from '../../services/httpInterceptor';

export const getAuthors = async () => {
  const response = await api.get('/autores');
  return response.data;
};

export const getAuthorById = async (id) => {
  const response = await api.get(`/autores/${id}`);
  return response.data;
};

export const createAuthor = async (data) => {
  const response = await api.post('/autores', data);
  return response.data;
};

export const updateAuthor = async (id, data) => {
  const response = await api.put(`/autores/${id}`, data);
  return response.data;
};

export const deleteAuthor = async (id) => {
  const response = await api.delete(`/autores/${id}`);
  return response.data;
};
