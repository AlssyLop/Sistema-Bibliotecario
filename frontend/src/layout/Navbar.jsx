import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom px-4 shadow-sm">
      <div className="container-fluid">
        <span className="navbar-brand mb-0 h1">Politécnico de la Costa Atlántica</span>
        <div className="d-flex align-items-center">
          <div className="text-secondary">
            <i className="bi bi-person-circle fs-4"></i>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
