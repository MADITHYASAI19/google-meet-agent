import React, { useState } from 'react';
import { Card, Badge } from '../ui/common';
import { LuSearch, LuFilter } from 'react-icons/lu';

const MeetingTable = ({ meetings = [], onSelect }) => (
  <div className="overflow-x-auto">
    <table className="w-full text-left">
      <thead>
        <tr className="border-b border-gray-200 dark:border-gray-700 text-sm text-gray-500 dark:text-gray-400">
          <th className="px-4 py-3 font-medium">Meeting ID</th>
          <th className="px-4 py-3 font-medium">Status</th>
          <th className="px-4 py-3 font-medium">Duration</th>
          <th className="px-4 py-3 font-medium">Date</th>
          <th className="px-4 py-3 font-medium text-right">Action</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
        {meetings.map((m) => (
          <tr key={m.meeting_id} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group">
            <td className="px-4 py-4 text-sm font-medium dark:text-white">{m.meeting_id.slice(0, 8)}...</td>
            <td className="px-4 py-4">
              <Badge color={m.status === 'active' ? 'success' : 'secondary'}>{m.status}</Badge>
            </td>
            <td className="px-4 py-4 text-sm text-gray-500 dark:text-gray-400">{m.duration || 'N/A'}</td>
            <td className="px-4 py-4 text-sm text-gray-500 dark:text-gray-400">{m.start_time || 'N/A'}</td>
            <td className="px-4 py-4 text-right">
              <button
                onClick={() => onSelect(m.meeting_id)}
                className="text-sm text-primary-600 font-semibold hover:underline"
              >
                Open
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default MeetingTable;
