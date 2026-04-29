
import React from 'react';

const Loader: React.FC = () => {
  return (
    <div className="w-24 h-24 relative">
      <div className="absolute inset-0 border-4 border-cyan-500/30 rounded-full"></div>
      <div className="absolute inset-0 border-4 border-t-cyan-400 border-l-cyan-400 border-b-transparent border-r-transparent rounded-full animate-spin"></div>
      <div className="absolute inset-2 border-2 border-cyan-500/20 rounded-full animate-pulse"></div>
    </div>
  );
};

export default Loader;
