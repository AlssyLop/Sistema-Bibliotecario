import React from 'react';

const ToastContainer = ({ toasts, removeToast }) => {
  return (
    <div className="toast-container position-fixed bottom-0 end-0 p-3" style={{ zIndex: 1100 }}>
      {toasts.map(toast => (
        <div key={toast.id} className={`toast show align-items-center text-bg-${toast.type} border-0 mb-2`} role="alert" aria-live="assertive" aria-atomic="true">
          <div className="d-flex">
            <div className="toast-body">
              {toast.message}
            </div>
            <button type="button" className="btn-close btn-close-white me-2 m-auto" onClick={() => removeToast(toast.id)} aria-label="Close"></button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ToastContainer;
