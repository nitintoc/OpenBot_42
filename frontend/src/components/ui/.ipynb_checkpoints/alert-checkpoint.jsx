// src/components/ui/alert.jsx
import React from 'react';

export const Alert = ({ children, type = 'info' }) => {
  const alertStyles = {
    info: 'bg-blue-100 text-blue-700',
    warning: 'bg-yellow-100 text-yellow-700',
    error: 'bg-red-100 text-red-700',
    success: 'bg-green-100 text-green-700',
  };

  return (
    <div className={`p-4 mb-4 border-l-4 ${alertStyles[type]}`}>
      {children}
    </div>
  );
};

export const AlertDescription = ({ children }) => (
  <p>{children}</p>
);
