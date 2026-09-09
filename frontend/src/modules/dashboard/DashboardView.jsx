import React, { useState, useEffect } from 'react';
import { getDashboardMetrics } from './dashboard.service';

const DashboardView = () => {
  const [metrics, setMetrics] = useState({
    total_estudiantes: 0,
    total_autores: 0,
    total_libros: 0,
    prestamos_activos: 0,
    devoluciones_pendientes: 0
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getDashboardMetrics();
        setMetrics(data);
      } catch (error) {
        console.error("Error fetching dashboard metrics:", error);
      }
    };
    fetchMetrics();
  }, []);

  return (
    <div>
      <h2 className="mb-4">Dashboard</h2>
      
      <div className="row g-4">
        <div className="col-md-4">
          <div className="card bg-primary text-white h-100">
            <div className="card-body d-flex flex-column align-items-center justify-content-center">
              <i className="bi bi-people display-4 mb-2"></i>
              <h5 className="card-title">Estudiantes</h5>
              <h2 className="display-6 fw-bold">{metrics.total_estudiantes}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card bg-success text-white h-100">
            <div className="card-body d-flex flex-column align-items-center justify-content-center">
              <i className="bi bi-pen display-4 mb-2"></i>
              <h5 className="card-title">Autores</h5>
              <h2 className="display-6 fw-bold">{metrics.total_autores}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card bg-info text-white h-100">
            <div className="card-body d-flex flex-column align-items-center justify-content-center">
              <i className="bi bi-book display-4 mb-2"></i>
              <h5 className="card-title">Libros Totales</h5>
              <h2 className="display-6 fw-bold">{metrics.total_libros}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card text-bg-warning h-100">
            <div className="card-body d-flex flex-column align-items-center justify-content-center">
              <i className="bi bi-clock-history display-4 mb-2"></i>
              <h5 className="card-title">Préstamos Activos</h5>
              <h2 className="display-6 fw-bold">{metrics.prestamos_activos}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card text-bg-danger h-100">
            <div className="card-body d-flex flex-column align-items-center justify-content-center">
              <i className="bi bi-exclamation-triangle display-4 mb-2"></i>
              <h5 className="card-title">Devoluciones Pendientes</h5>
              <h2 className="display-6 fw-bold">{metrics.devoluciones_pendientes}</h2>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardView;
