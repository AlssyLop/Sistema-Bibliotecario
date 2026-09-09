import React, { useState, useEffect } from 'react';
import { getActiveLoans, getPendingLoans, createLoan, returnLoan } from './loans.service';
import { getStudents } from '../students/students.service';
import { getBooks } from '../books/books.service';
import LoanFormModal from './LoanFormModal';
import ConfirmDialog from '../../components/shared/ConfirmDialog';

const LoansView = () => {
  const [activeLoans, setActiveLoans] = useState([]);
  const [pendingLoans, setPendingLoans] = useState([]);
  const [students, setStudents] = useState([]);
  const [books, setBooks] = useState([]);
  const [tab, setTab] = useState('active'); // 'active' or 'pending'
  
  const [showModal, setShowModal] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loanToReturn, setLoanToReturn] = useState(null);

  const fetchData = async () => {
    try {
      const [active, pending, studs, bks] = await Promise.all([
        getActiveLoans(),
        getPendingLoans(),
        getStudents(),
        getBooks()
      ]);
      setActiveLoans(active);
      setPendingLoans(pending);
      setStudents(studs);
      setBooks(bks);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSave = async (data) => {
    try {
      await createLoan(data);
      setShowModal(false);
      fetchData();
    } catch (error) {
      console.error("Error saving loan:", error);
    }
  };

  const handleReturnConfirm = async () => {
    try {
      await returnLoan(loanToReturn.id);
      setShowConfirm(false);
      fetchData();
    } catch (error) {
      console.error("Error returning loan:", error);
    }
  };

  const renderTable = (loans) => (
    <div className="card p-3 mt-3">
      <table className="table table-hover align-middle">
        <thead>
          <tr>
            <th>Estudiante</th>
            <th>Libro</th>
            <th>Fecha Salida</th>
            <th>Fecha Pactada</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {loans.map(loan => (
            <tr key={loan.id}>
              <td>{loan.estudiante?.nombre_completo}</td>
              <td>{loan.libro?.titulo}</td>
              <td>{new Date(loan.fecha_salida).toLocaleString()}</td>
              <td>{new Date(loan.fecha_pactada).toLocaleString()}</td>
              <td>
                <span className={`badge ${loan.estado_prestamo === 'Activo' ? 'text-bg-primary' : loan.estado_prestamo === 'Atrasado' ? 'text-bg-danger' : 'text-bg-success'}`}>
                  {loan.estado_prestamo}
                </span>
              </td>
              <td>
                {(loan.estado_prestamo === 'Activo' || loan.estado_prestamo === 'Atrasado') && (
                  <button className="btn btn-sm btn-success" onClick={() => { setLoanToReturn(loan); setShowConfirm(true); }}>
                    <i className="bi bi-box-arrow-in-down me-1"></i> Devolver
                  </button>
                )}
              </td>
            </tr>
          ))}
          {loans.length === 0 && (
            <tr>
              <td colSpan="6" className="text-center">No hay préstamos en esta categoría.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Historial de Préstamos</h2>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <i className="bi bi-plus-circle me-2"></i> Registrar Préstamo
        </button>
      </div>

      <ul className="nav nav-tabs">
        <li className="nav-item">
          <button className={`nav-link ${tab === 'active' ? 'active' : ''}`} onClick={() => setTab('active')}>
            Préstamos Activos
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${tab === 'pending' ? 'active text-danger' : 'text-danger'}`} onClick={() => setTab('pending')}>
            Devoluciones Pendientes
          </button>
        </li>
      </ul>

      {tab === 'active' ? renderTable(activeLoans) : renderTable(pendingLoans)}

      <LoanFormModal
        show={showModal}
        students={students}
        books={books}
        onClose={() => setShowModal(false)}
        onSave={handleSave}
      />

      <ConfirmDialog
        show={showConfirm}
        title="Registrar Devolución"
        message={`¿Confirmas la devolución del libro "${loanToReturn?.libro?.titulo}" por parte de ${loanToReturn?.estudiante?.nombre_completo}?`}
        onConfirm={handleReturnConfirm}
        onCancel={() => setShowConfirm(false)}
      />
    </div>
  );
};

export default LoansView;
