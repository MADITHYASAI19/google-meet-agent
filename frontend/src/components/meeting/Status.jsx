import React from 'react';
import { Card, Badge } from '../ui/common';
import { LuClock, LuCheckCircle, LuAlertCircle, LuPlayCircle } from 'react-icons/lu';

export const MeetingStatus = ({ status, className = '' }) => {
  const config = {
    'active': { color: 'success', icon: <LuPlayCircle />, label: 'Running' },
    'completed': { color: 'success', icon: <LuCheckCircle />, label: 'Completed' },
    'failed': { color: 'danger', icon: <LuAlertCircle />, label: 'Failed' },
    'joining': { color: 'warning', icon: <LuClock />, label: 'Joining...' },
  };

  const { color, icon, label } = config[status] || { color: 'secondary', icon: <LuClock />, label: status };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-gray-500 dark:text-gray-400">{icon}</span>
      <Badge color={color}>{label}</Badge>
    </div>
  );
};

export const MeetingProgress = ({ stage, progress = 0 }) => (
  <div className="w-full space-y-2">
    <div className="flex justify-between text-xs font-medium text-gray-500 dark:text-gray-400">
      <span>{stage}</span>
      <span>{Math.round(progress)}%</span>
    </div>
    <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
      <div
        className="h-full bg-primary-600 transition-all duration-500 ease-out"
        style={{ width: `${progress}%` }}
      />
    </div>
  </div>
);
