import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="sidebar p-3 d-flex flex-column" style={{ width: '250px' }}>
      <div className="text-center mb-4">
        <h4 className="text-white">PCA Library</h4>
        <hr className="bg-secondary" />
      </div>
      <nav className="nav flex-column gap-2">
        <NavLink to="/dashboard" className={({isActive}) => isActive ? "active" : ""}>
          <i className="bi bi-speedometer2 me-2"></i> Dashboard
        </NavLink>
        <NavLink to="/authors" className={({isActive}) => isActive ? "active" : ""}>
          <i className="bi bi-pen me-2"></i> Autores
        </NavLink>
        <NavLink to="/students" className={({isActive}) => isActive ? "active" : ""}>
          <i className="bi bi-people me-2"></i> Estudiantes
        </NavLink>
        <NavLink to="/books" className={({isActive}) => isActive ? "active" : ""}>
          <i className="bi bi-book me-2"></i> Libros
        </NavLink>
        <NavLink to="/loans" className={({isActive}) => isActive ? "active" : ""}>
          <i className="bi bi-clock-history me-2"></i> Préstamos
        </NavLink>
      </nav>
    </div>
  );
};

export default Sidebar;
