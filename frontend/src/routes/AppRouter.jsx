import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import AppShell from '../layout/AppShell';

// Lazy load modules
const DashboardView = lazy(() => import('../modules/dashboard/DashboardView'));
const AuthorsView = lazy(() => import('../modules/authors/AuthorsView'));
const StudentsView = lazy(() => import('../modules/students/StudentsView'));
const BooksView = lazy(() => import('../modules/books/BooksView'));
const LoansView = lazy(() => import('../modules/loans/LoansView'));

const LoadingFallback = () => (
  <div className="d-flex justify-content-center align-items-center" style={{ height: '200px' }}>
    <div className="spinner-border text-primary" role="status">
      <span className="visually-hidden">Cargando...</span>
    </div>
  </div>
);

const AppRouter = () => {
  return (
    <AppShell>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardView />} />
          <Route path="/authors" element={<AuthorsView />} />
          <Route path="/students" element={<StudentsView />} />
          <Route path="/books" element={<BooksView />} />
          <Route path="/loans" element={<LoansView />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Suspense>
    </AppShell>
  );
};

export default AppRouter;
