import React, { useState, useEffect } from 'react';
import { getBooks, createBook, updateBook, deleteBook } from './books.service';
import { getAuthors } from '../authors/authors.service';
import BookFormModal from './BookFormModal';
import ConfirmDialog from '../../components/shared/ConfirmDialog';

const BooksView = () => {
  const [books, setBooks] = useState([]);
  const [authors, setAuthors] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingBook, setEditingBook] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [bookToDelete, setBookToDelete] = useState(null);

  const fetchData = async () => {
    try {
      const [booksData, authorsData] = await Promise.all([
        getBooks(),
        getAuthors()
      ]);
      setBooks(booksData);
      setAuthors(authorsData);
    } catch (error) {
      console.error("Error fetching books/authors:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSave = async (data) => {
    try {
      if (editingBook) {
        await updateBook(editingBook.id, data);
      } else {
        await createBook(data);
      }
      setShowModal(false);
      fetchData();
    } catch (error) {
      console.error("Error saving book:", error);
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      await deleteBook(bookToDelete.id);
      setShowConfirm(false);
      fetchData();
    } catch (error) {
      console.error("Error deleting book:", error);
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Gestión de Libros</h2>
        <button className="btn btn-primary" onClick={() => { setEditingBook(null); setShowModal(true); }}>
          <i className="bi bi-plus-circle me-2"></i> Nuevo Libro
        </button>
      </div>

      <div className="card p-3">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th>ISBN</th>
              <th>Título</th>
              <th>Autor</th>
              <th>Categoría</th>
              <th>Ejemplares</th>
              <th>Disponibles</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {books.map(book => (
              <tr key={book.id}>
                <td>{book.isbn}</td>
                <td>{book.titulo}</td>
                <td>{book.autor ? book.autor.nombre_completo : '-'}</td>
                <td>{book.categoria}</td>
                <td>{book.cantidad_total}</td>
                <td>
                  <span className={`badge ${book.cantidad_disponible > 0 ? 'text-bg-success' : 'text-bg-danger'}`}>
                    {book.cantidad_disponible}
                  </span>
                </td>
                <td>
                  <button className="btn btn-sm btn-outline-secondary me-2" onClick={() => { setEditingBook(book); setShowModal(true); }}>
                    <i className="bi bi-pencil"></i>
                  </button>
                  <button className="btn btn-sm btn-outline-danger" onClick={() => { setBookToDelete(book); setShowConfirm(true); }}>
                    <i className="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            ))}
            {books.length === 0 && (
              <tr>
                <td colSpan="7" className="text-center">No hay libros registrados.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <BookFormModal
        show={showModal}
        book={editingBook}
        authors={authors}
        onClose={() => setShowModal(false)}
        onSave={handleSave}
      />

      <ConfirmDialog
        show={showConfirm}
        title="Eliminar Libro"
        message={`¿Estás seguro de eliminar el libro "${bookToDelete?.titulo}"?`}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setShowConfirm(false)}
      />
    </div>
  );
};

export default BooksView;
