import React from 'react';
import { Card, Badge } from '../ui/common';
import { LuBook, LuClock, LuCpu, LuHash } from 'react-icons/lu';

const NotesStatistics = ({ stats }) => {
  const items = [
    { icon: <LuHash />, label: 'Word Count', value: stats.word_count || '0', color: 'text-blue-500' },
    { icon: <LuBook />, label: 'Paragraphs', value: stats.paragraph_count || '0', color: 'text-green-500' },
    { icon: <LuClock />, label: 'Reading Time', value: `${stats.reading_time || 0} min`, color: 'text-orange-500' },
    { icon: <LuCpu />, label: 'Model', value: stats.model || 'Unknown', color: 'text-purple-500' },
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

const NotesMetadata = ({ metadata }) => {
  return (
    <Card className="p-4 bg-gray-50 dark:bg-gray-800/50 border-dashed">
      <h4 className="text-xs font-bold text-gray-400 uppercase mb-3">Generation Metadata</h4>
      <div className="grid grid-cols-2 gap-y-2 text-xs">
        <span className="text-gray-500">Provider:</span>
        <span className="text-right dark:text-white font-medium">{metadata.provider || 'N/A'}</span>
        <span className="text-gray-500">Timestamp:</span>
        <span className="text-right dark:text-white font-medium">{metadata.timestamp || 'N/A'}</span>
        <span className="text-gray-500">Tokens:</span>
        <span className="text-right dark:text-white font-medium">{metadata.tokens || 'N/A'}</span>
        <span className="text-gray-500">Version:</span>
        <span className="text-right dark:text-white font-medium">{metadata.version || '1.0'}</span>
      </div}
    </Card>
  );
};

export { NotesStatistics, NotesMetadata };
