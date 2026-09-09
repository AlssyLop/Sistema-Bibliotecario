import React from 'react';

const ConfirmDialog = ({ show, title, message, onConfirm, onCancel }) => {
  if (!show) return null;

  return (
    <>
      <div className="modal-backdrop fade show"></div>
      <div className="modal fade show d-block" tabIndex="-1">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header text-bg-danger">
              <h5 className="modal-title">{title}</h5>
              <button type="button" className="btn-close btn-close-white" onClick={onCancel}></button>
            </div>
            <div className="modal-body">
              <p>{message}</p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={onConfirm}>Confirmar</button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ConfirmDialog;
