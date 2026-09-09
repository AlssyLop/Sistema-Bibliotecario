import React, { useState, useEffect } from 'react';

const LoanFormModal = ({ show, onClose, onSave, students, books }) => {
  const [formData, setFormData] = useState({
    estudiante_id: '',
    libro_id: '',
    fecha_pactada: ''
  });

  useEffect(() => {
    setFormData({ estudiante_id: '', libro_id: '', fecha_pactada: '' });
  }, [show]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      ...formData,
      fecha_salida: new Date().toISOString()
    });
  };

  if (!show) return null;

  return (
    <>
      <div className="modal-backdrop fade show"></div>
      <div className="modal fade show d-block" tabIndex="-1">
        <div className="modal-dialog">
          <form className="modal-content" onSubmit={handleSubmit}>
            <div className="modal-header">
              <h5 className="modal-title">Registrar Préstamo</h5>
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Estudiante <span className="text-danger">*</span></label>
                <select className="form-select" name="estudiante_id" value={formData.estudiante_id} onChange={handleChange} required>
                  <option value="">Seleccione un estudiante...</option>
                  {students.filter(s => s.estado).map(s => (
                    <option key={s.id} value={s.id}>{s.nombre_completo} ({s.documento_identidad})</option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label">Libro <span className="text-danger">*</span></label>
                <select className="form-select" name="libro_id" value={formData.libro_id} onChange={handleChange} required>
                  <option value="">Seleccione un libro...</option>
                  {books.filter(b => b.cantidad_disponible > 0).map(b => (
                    <option key={b.id} value={b.id}>{b.titulo} - Dispo: {b.cantidad_disponible}</option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label">Fecha Pactada de Devolución <span className="text-danger">*</span></label>
                <input type="datetime-local" className="form-control" name="fecha_pactada" value={formData.fecha_pactada} onChange={handleChange} required />
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-primary">Registrar</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default LoanFormModal;
