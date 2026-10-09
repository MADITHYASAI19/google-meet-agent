import React from 'react';
import { Card, Badge } from '../ui/common';
import { LuCalendar, LuPlay, LuCheckCircle } from 'react-icons/lu';

const MeetingCard = ({ meeting, onSelect }) => (
  <Card className="hover:shadow-md transition-all cursor-pointer group" onClick={() => onSelect(meeting.meeting_id)}>
    <div className="flex justify-between items-start mb-4">
      <div className="w-10 h-10 rounded-xl bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-600 dark:text-primary-400 font-bold">
        {meeting.meeting_id.charAt(0).toUpperCase()}
      </div>
      <Badge color={meeting.status === 'active' ? 'success' : 'secondary'}>{meeting.status}</Badge>
    </div>
    <h3 className="font-bold text-gray-900 dark:text-white mb-1 truncate">
      {meeting.title || `Meeting ${meeting.meeting_id.slice(0, 6)}`}
    </h3>
    <div className="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400 mt-4">
      <span className="flex items-center gap-1"><LuCalendar /> {meeting.start_time || 'N/A'}</span>
      <span className="flex items-center gap-1"><LuClock /> {meeting.duration || '0m'}</span>
    </div>
  </Card>
);

export default MeetingCard;
