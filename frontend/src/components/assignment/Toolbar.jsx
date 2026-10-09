import React from 'react';
import { LuDownload, LuCopy, LuMaximize, LuSearch, LuPrinter } from 'react-icons/lu';

const AssignmentToolbar = ({ onSearch, onDownload, onCopy, onPrint }) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-dark-card sticky top-0 z-10">
      <div className="flex items-center gap-2 relative flex-1 max-w-md">
        <LuSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search questions..."
          className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          onChange={(e) => onSearch(e.target.value)}
        />
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={onCopy}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title="Copy Assignment"
        >
          <LuCopy size={18} />
        </button>
        <button
          onClick={onDownload}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title="Download PDF"
        >
          <LuDownload size={18} />
        </button>
        <button
          onClick={onPrint}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title="Print"
        >
          <LuPrinter size={18} />
        </button>
        <button
          onClick={() => document.documentElement.requestFullscreen()}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title="Fullscreen"
        >
          <LuMaximize size={18} />
        </button>
      </div>
    </nav>
  );
};

export default AssignmentToolbar;
