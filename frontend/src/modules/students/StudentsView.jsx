import React, { useState, useEffect } from 'react';
import { getStudents, createStudent, updateStudent, deleteStudent } from './students.service';
import StudentFormModal from './StudentFormModal';
import ConfirmDialog from '../../components/shared/ConfirmDialog';

const StudentsView = () => {
  const [students, setStudents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [studentToDelete, setStudentToDelete] = useState(null);

  const fetchStudents = async () => {
    try {
      const data = await getStudents();
      setStudents(data);
    } catch (error) {
      console.error("Error fetching students:", error);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleSave = async (data) => {
    try {
      if (editingStudent) {
        await updateStudent(editingStudent.id, data);
      } else {
        await createStudent(data);
      }
      setShowModal(false);
      fetchStudents();
    } catch (error) {
      console.error("Error saving student:", error);
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      await deleteStudent(studentToDelete.id);
      setShowConfirm(false);
      fetchStudents();
    } catch (error) {
      console.error("Error deleting student:", error);
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Gestión de Estudiantes</h2>
        <button className="btn btn-primary" onClick={() => { setEditingStudent(null); setShowModal(true); }}>
          <i className="bi bi-plus-circle me-2"></i> Nuevo Estudiante
        </button>
      </div>

      <div className="card p-3">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th>Documento</th>
              <th>Nombre</th>
              <th>Correo</th>
              <th>Carrera</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {students.map(student => (
              <tr key={student.id}>
                <td>{student.documento_identidad}</td>
                <td>{student.nombre_completo}</td>
                <td>{student.correo_institucional}</td>
                <td>{student.carrera}</td>
                <td>
                  <span className={`badge ${student.estado ? 'text-bg-success' : 'text-bg-danger'}`}>
                    {student.estado ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
                <td>
                  <button className="btn btn-sm btn-outline-secondary me-2" onClick={() => { setEditingStudent(student); setShowModal(true); }}>
                    <i className="bi bi-pencil"></i>
                  </button>
                  <button className="btn btn-sm btn-outline-danger" onClick={() => { setStudentToDelete(student); setShowConfirm(true); }}>
                    <i className="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            ))}
            {students.length === 0 && (
              <tr>
                <td colSpan="6" className="text-center">No hay estudiantes registrados.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <StudentFormModal
        show={showModal}
        student={editingStudent}
        onClose={() => setShowModal(false)}
        onSave={handleSave}
      />

      <ConfirmDialog
        show={showConfirm}
        title="Inhabilitar Estudiante"
        message={`¿Estás seguro de inhabilitar a ${studentToDelete?.nombre_completo}?`}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setShowConfirm(false)}
      />
    </div>
  );
};

export default StudentsView;
