import React, { useState } from 'react';
import { Card } from '../ui/common';
import { LuChevronDown, LuChevronUp } from 'react-icons/lu';

const AssignmentRubric = ({ rubric }) => {
  const [expanded, setExpanded] = useState(true);

  if (!rubric) return null;

  return (
    <Card className="overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <h3 className="font-bold text-gray-900 dark:text-white flex items-center gap-2">
          Grading Rubric
        </h3>
        {expanded ? <LuChevronUp /> : <LuChevronDown />}
      </button>

      {expanded && (
        <div className="p-4 overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-gray-500 uppercase text-xs border-b border-gray-200 dark:border-gray-700">
              <tr>
                <th className="py-2">Criteria</th>
                <th className="py-2 text-center">Excellent</th>
                <th className="py-2 text-center">Good</th>
                <th className="py-2 text-center">Needs Work</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
              {rubric.criteria?.map((c, i) => (
                <tr key={i}>
                  <td className="py-3 font-medium dark:text-white">{c.name}</td>
                  <td className="py-3 text-center text-gray-600 dark:text-gray-400">{c.excellent}</td>
                  <td className="py-3 text-center text-gray-600 dark:text-gray-400">{c.good}</td>
                  <td className="py-3 text-center text-gray-600 dark:text-gray-400">{c.poor}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
};

export default AssignmentRubric;
