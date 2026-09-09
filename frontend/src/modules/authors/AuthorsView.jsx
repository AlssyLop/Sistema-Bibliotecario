import React, { useState, useEffect } from 'react';
import { getAuthors, createAuthor, updateAuthor, deleteAuthor } from './authors.service';
import AuthorFormModal from './AuthorFormModal';
import ConfirmDialog from '../../components/shared/ConfirmDialog';

const AuthorsView = () => {
  const [authors, setAuthors] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingAuthor, setEditingAuthor] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [authorToDelete, setAuthorToDelete] = useState(null);

  const fetchAuthors = async () => {
    try {
      const data = await getAuthors();
      setAuthors(data);
    } catch (error) {
      console.error("Error fetching authors:", error);
    }
  };

  useEffect(() => {
    fetchAuthors();
  }, []);

  const handleSave = async (authorData) => {
    try {
      if (editingAuthor) {
        await updateAuthor(editingAuthor.id, authorData);
      } else {
        await createAuthor(authorData);
      }
      setShowModal(false);
      fetchAuthors();
    } catch (error) {
      console.error("Error saving author:", error);
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      await deleteAuthor(authorToDelete.id);
      setShowConfirm(false);
      fetchAuthors();
    } catch (error) {
      console.error("Error deleting author:", error);
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Gestión de Autores</h2>
        <button className="btn btn-primary" onClick={() => { setEditingAuthor(null); setShowModal(true); }}>
          <i className="bi bi-plus-circle me-2"></i> Nuevo Autor
        </button>
      </div>

      <div className="card p-3">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th>Documento</th>
              <th>Nombre Completo</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {authors.map(author => (
              <tr key={author.id}>
                <td>{author.documento_identidad}</td>
                <td>{author.nombre_completo}</td>
                <td>{author.correo || '-'}</td>
                <td>{author.telefono || '-'}</td>
                <td>
                  <button className="btn btn-sm btn-outline-secondary me-2" onClick={() => { setEditingAuthor(author); setShowModal(true); }}>
                    <i className="bi bi-pencil"></i>
                  </button>
                  <button className="btn btn-sm btn-outline-danger" onClick={() => { setAuthorToDelete(author); setShowConfirm(true); }}>
                    <i className="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            ))}
            {authors.length === 0 && (
              <tr>
                <td colSpan="5" className="text-center">No hay autores registrados.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <AuthorFormModal
        show={showModal}
        author={editingAuthor}
        onClose={() => setShowModal(false)}
        onSave={handleSave}
      />

      <ConfirmDialog
        show={showConfirm}
        title="Eliminar Autor"
        message={`¿Estás seguro de eliminar a ${authorToDelete?.nombre_completo}?`}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setShowConfirm(false)}
      />
    </div>
  );
};

export default AuthorsView;
