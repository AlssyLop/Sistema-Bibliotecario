import api from '../../services/httpInterceptor';

export const getStudents = async () => {
  const response = await api.get('/estudiantes');
  return response.data;
};

export const createStudent = async (data) => {
  const response = await api.post('/estudiantes', data);
  return response.data;
};

export const updateStudent = async (id, data) => {
  const response = await api.put(`/estudiantes/${id}`, data);
  return response.data;
};

export const deleteStudent = async (id) => {
  const response = await api.delete(`/estudiantes/${id}`);
  return response.data;
};
