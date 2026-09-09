import React, { useState, useEffect } from 'react';

const BookFormModal = ({ show, onClose, onSave, book, authors }) => {
  const [formData, setFormData] = useState({
    isbn: '',
    titulo: '',
    autor_id: '',
    editorial: '',
    anio_publicacion: '',
    categoria: '',
    cantidad_total: ''
  });

  useEffect(() => {
    if (book) {
      setFormData({
        isbn: book.isbn || '',
        titulo: book.titulo || '',
        autor_id: book.autor_id || '',
        editorial: book.editorial || '',
        anio_publicacion: book.anio_publicacion || '',
        categoria: book.categoria || '',
        cantidad_total: book.cantidad_total || ''
      });
    } else {
      setFormData({ isbn: '', titulo: '', autor_id: '', editorial: '', anio_publicacion: '', categoria: '', cantidad_total: '' });
    }
  }, [book, show]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      ...formData,
      anio_publicacion: parseInt(formData.anio_publicacion),
      cantidad_total: parseInt(formData.cantidad_total)
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
              <h5 className="modal-title">{book ? 'Editar Libro' : 'Registrar Libro'}</h5>
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">ISBN <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="isbn" value={formData.isbn} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Título <span className="text-danger">*</span></label>
                <input type="text" className="form-control" name="titulo" value={formData.titulo} onChange={handleChange} required />
              </div>
              <div className="mb-3">
                <label className="form-label">Autor <span className="text-danger">*</span></label>
                <select className="form-select" name="autor_id" value={formData.autor_id} onChange={handleChange} required>
                  <option value="">Seleccione un autor...</option>
                  {authors.map(a => (
                    <option key={a.id} value={a.id}>{a.nombre_completo}</option>
                  ))}
                </select>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Editorial <span className="text-danger">*</span></label>
                  <input type="text" className="form-control" name="editorial" value={formData.editorial} onChange={handleChange} required />
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Año <span className="text-danger">*</span></label>
                  <input type="number" className="form-control" name="anio_publicacion" value={formData.anio_publicacion} onChange={handleChange} required />
                </div>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Categoría <span className="text-danger">*</span></label>
                  <input type="text" className="form-control" name="categoria" value={formData.categoria} onChange={handleChange} required />
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Ejemplares Totales <span className="text-danger">*</span></label>
                  <input type="number" min="0" className="form-control" name="cantidad_total" value={formData.cantidad_total} onChange={handleChange} required />
                </div>
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

export default BookFormModal;
