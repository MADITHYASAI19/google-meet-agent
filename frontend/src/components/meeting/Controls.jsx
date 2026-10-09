import React from 'react';
import { Button, Card } from '../ui/common';
import { LuPlay, LuSquare, LuRefreshCw, LuDownload, LuFileText } from 'react-icons/lu';
import apiClient from '../../api/client';

const MeetingControls = ({ meetingId, onAction }) => {
  const handleAction = async (endpoint, label) => {
    try {
      await apiClient.post(`/meetings/${meetingId}${endpoint}`);
      if (onAction) onAction(label);
    } catch (err) {
      alert(`Error: ${err.response?.data?.message || 'Action failed'}`);
    }
  };

  return (
    <div className="flex flex-wrap gap-3">
      <Button onClick={() => handleAction('/join', 'Join')} className="flex items-center gap-2">
        <LuPlay /> Join
      </Button>
      <Button variant="outline" onClick={() => handleAction('/leave', 'Leave')} className="flex items-center gap-2">
        <LuSquare /> Leave
      </Button>
      <Button variant="secondary" onClick={() => window.location.reload()} className="flex items-center gap-2">
        <LuRefreshCw /> Refresh
      </Button>
      <Button variant="outline" onClick={() => window.location.href = `/meetings/${meetingId}`} className="flex items-center gap-2">
        <LuFileText /> Details
      </Button>
      <Button variant="secondary" onClick={() => window.open(`/api/v1/audio/${meetingId}/download`)} className="flex items-center gap-2">
        <LuDownload /> Audio
      </Button>
    </div>
  );
};

export default MeetingControls;
