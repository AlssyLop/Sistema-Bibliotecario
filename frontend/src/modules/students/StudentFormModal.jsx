import React, { useState, useEffect } from 'react';

const StudentFormModal = ({ show, onClose, onSave, student }) => {
  const [formData, setFormData] = useState({
    documento_identidad: '',
    nombre_completo: '',
    correo_institucional: '',
    telefono: '',
    carrera: ''
  });

  useEffect(() => {
    if (student) {
      setFormData({
        documento_identidad: student.documento_identidad || '',
        nombre_completo: student.nombre_completo || '',
        correo_institucional: student.correo_institucional || '',
        telefono: student.telefono || '',
        carrera: student.carrera || ''
      });
    } else {
      setFormData({ documento_identidad: '', nombre_completo: '', correo_institucional: '', telefono: '', carrera: '' });
    }
  }, [student, show]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  if (!show) return null;

  return (
    <>
      <div className="modal-backdrop fade show"></div>
      <div className="modal fade show d-block" tabIndex="-1">
        <div className="modal-dialog">
          <form className="modal-content" onSubmit={handleSubmit}>
            <div className="modal-header">
              <h5 className="modal-title">{student ? 'Editar Estudiante' : 'Registrar Estudiante'}</h5>
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Documento <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="documento_identidad" value={formData.documento_identidad} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Nombre Completo <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="nombre_completo" value={formData.nombre_completo} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Correo Institucional (@pca.edu.co) <span className="text-danger">*</span></label>
                <input type="email" className="form-control" name="correo_institucional" value={formData.correo_institucional} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Carrera <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="carrera" value={formData.carrera} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Teléfono</label>
                <input type="text" className="form-control" name="telefono" value={formData.telefono} onChange={handleChange} />
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-primary">Guardar</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default StudentFormModal;
