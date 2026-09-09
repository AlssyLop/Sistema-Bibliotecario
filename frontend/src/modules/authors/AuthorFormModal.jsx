import React, { useState, useEffect } from 'react';

const AuthorFormModal = ({ show, onClose, onSave, author }) => {
  const [formData, setFormData] = useState({
    documento_identidad: '',
    nombre_completo: '',
    correo: '',
    telefono: ''
  });

  useEffect(() => {
    if (author) {
      setFormData({
        documento_identidad: author.documento_identidad || '',
        nombre_completo: author.nombre_completo || '',
        correo: author.correo || '',
        telefono: author.telefono || ''
      });
    } else {
      setFormData({ documento_identidad: '', nombre_completo: '', correo: '', telefono: '' });
    }
  }, [author, show]);

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
              <h5 className="modal-title">{author ? 'Editar Autor' : 'Registrar Autor'}</h5>
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Documento de Identidad <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="documento_identidad" value={formData.documento_identidad} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Nombre Completo <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="nombre_completo" value={formData.nombre_completo} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Correo</label>
                <input type="email" className="form-control" name="correo" value={formData.correo} onChange={handleChange} />
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

export default AuthorFormModal;
