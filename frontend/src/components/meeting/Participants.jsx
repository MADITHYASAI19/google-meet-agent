import React from 'react';
import { Card, Badge } from '../ui/common';
import { LuUser, LuClock } from 'react-icons/lu';

const ParticipantCard = ({ participant }) => (
  <div className="flex items-center justify-between p-3 rounded-xl border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-600 dark:text-primary-400 text-xs font-bold">
        {participant.name?.charAt(0) || 'U'}
      </div>
      <div>
        <p className="text-sm font-medium dark:text-white">{participant.name}</p>
        <p className="text-xs text-gray-500">{participant.role || 'Student'}</p>
      </div>
    </div>
    <div className="flex items-center gap-4 text-xs text-gray-500">
      <span className="flex items-center gap-1"><LuClock /> {participant.join_time}</span>
      <Badge color={participant.status === 'present' ? 'success' : 'danger'}>
        {participant.status}
      </Badge>
    </div>
  </div>
);

const MeetingParticipants = ({ participants = [] }) => (
  <div className="flex flex-col gap-4">
    <div className="flex justify-between items-center">
      <h3 className="text-lg font-bold dark:text-white">Participants ({participants.length})</h3>
      <input
        type="text"
        placeholder="Search participants..."
        className="px-3 py-1 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-dark-card dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
      />
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      {participants.length > 0 ? (
        participants.map((p, i) => <ParticipantCard key={i} participant={p} />)
      ) : (
        <p className="text-sm text-gray-500 italic">No participants recorded yet.</p>
      )}
    </div>
  </div>
);

export default MeetingParticipants;
