import React from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

const AppShell = ({ children }) => {
  return (
    <div className="d-flex w-100">
      <Sidebar />
      <div className="flex-grow-1 d-flex flex-column" style={{ minHeight: '100vh', width: '0' }}>
        <Navbar />
        <main className="p-4 flex-grow-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default AppShell;
