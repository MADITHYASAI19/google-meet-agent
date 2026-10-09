import React from 'react';
import { Card } from '../ui/common';
import { LuFileText, LuCpu, LuClock, LuHash } from 'react-icons/lu';

const AssignmentStatistics = ({ stats }) => {
  const items = [
    { icon: <LuHash />, label: 'Total Questions', value: stats.total_questions || '0', color: 'text-blue-500' },
    { icon: <LuFileText />, label: 'Total Marks', value: stats.total_marks || '0', color: 'text-green-500' },
    { icon: <LuClock />, label: 'Est. Time', value: `${stats.estimated_time || 0}m`, color: 'text-orange-500' },
    { icon: <LuCpu />, label: 'AI Model', value: stats.model || 'Unknown', color: 'text-purple-500' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {items.map((item, i) => (
        <Card key={i} className="text-center p-4">
          <div className={`flex justify-center mb-2 ${item.color}`}>{item.icon}</div>
          <p className="text-xs text-gray-500 dark:text-gray-400">{item.label}</p>
          <p className="text-lg font-bold dark:text-white">{item.value}</p>
        </Card>
      ))}
    </div>
  );
};

export default AssignmentStatistics;
