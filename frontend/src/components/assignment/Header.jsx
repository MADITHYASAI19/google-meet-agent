import React from 'react';
import { Badge } from '../ui/common';
import { LuClock, LuFileText, LuAward, LuLayers } from 'react-icons/lu';

const AssignmentHeader = ({ assignment }) => {
  return (
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          {assignment?.title || 'Lecture Assignment'}
        </h1>
        <div className="flex flex-wrap items-center gap-3">
          <Badge color="primary">{assignment?.difficulty || 'Medium'}</Badge>
          <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <LuFileText size={14} /> {assignment?.total_questions || 0} Questions
          </span>
          <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <LuAward size={14} /> {assignment?.total_marks || 0} Marks
          </span>
          <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
            <LuClock size={14} /> {assignment?.estimated_time || '30'} mins
          </span>
        </div>
      </div>
      <div className="text-right hidden md:block">
        <p className="text-xs text-gray-400 uppercase font-bold">Generated on</p>
        <p className="text-sm text-gray-600 dark:text-gray-300">{assignment?.generated_at || 'N/A'}</p>
      </div>
    </div>
  );
};

export default AssignmentHeader;
