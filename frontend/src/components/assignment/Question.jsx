import React from 'react';
import { Badge } from '../ui/common';

const AssignmentQuestion = ({ question, index }) => {
  const { text, marks, difficulty, instructions, type } = question;

  return (
    <div className="p-6 rounded-2xl border border-gray-100 dark:border-gray-700 bg-white dark:bg-dark-card mb-6 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-3">
          <span className="w-8 h-8 rounded-lg bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 flex items-center justify-center font-bold text-sm">
            {index + 1}
          </span>
          <Badge color="secondary">{type?.replace('_', ' ')}</Badge>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium text-gray-400">Marks: {marks}</span>
          <Badge color="primary">{difficulty}</Badge>
        </div>
      </div>
      <p className="text-lg font-medium text-gray-900 dark:text-white mb-4 leading-relaxed">
        {text}
      </p>
      {instructions && (
        <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border-l-4 border-primary-500">
          <p className="text-sm text-gray-600 dark:text-gray-400 italic">
            <strong>Instruction:</strong> {instructions}
          </p>
        </div>
      )}
    </div>
  );
};

export default AssignmentQuestion;
