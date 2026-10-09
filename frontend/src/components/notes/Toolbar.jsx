import React from 'react';
import { Card, Button, Badge } from '../ui/common';
import { LuDownload, LuCopy, LuMaximize, LuSearch, LuPrinter } from 'react-icons/lu';

const NotesToolbar = ({ onSearch, onDownload, onCopy, onPrint }) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-dark-card sticky top-0 z-10">
      <div className="flex items-center gap-2 relative flex-1 max-w-md">
        <LuSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search in notes..."
          className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
          onChange={(e) => onSearch(e.target.value)}
        />
      </div>

      <div className="flex items-center gap-2">
        <Button variant="secondary" onClick={onCopy} className="flex items-center gap-2 text-sm">
          <LuCopy /> Copy
        </Button>
        <Button variant="secondary" onClick={() => onDownload('md')} className="flex items-center gap-2 text-sm">
          <LuDownload /> Markdown
        </Button>
        <Button variant="secondary" onClick={onPrint} className="flex items-center gap-2 text-sm">
          <LuPrinter /> Print
        </Button>
        <Button variant="primary" onClick={() => document.documentElement.requestFullscreen()} className="flex items-center gap-2 text-sm">
          <LuMaximize /> Fullscreen
        </Button>
      </div>
    </nav>
  );
};

export default NotesToolbar;
