import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from '../ui/common';
import MeetingHeader from '../meeting/Header';
import MeetingControls from '../meeting/Controls';
import MeetingParticipants from '../meeting/Participants';
import { MeetingStatus, MeetingProgress } from '../meeting/Status';
import { useMeetingWebSocket } from '../../hooks/useMeetingWebSocket';
import apiClient from '../../api/client';
import { LuActivity, LuFileText, LuMic } from 'react-icons/lu';

const MeetingDetailsPage = () => {
  const { meetingId } = useParams();
  const [meeting, setMeeting] = useState(null);
  const { status, events, progress } = useMeetingWebSocket(meetingId);

  const fetchDetails = async () => {
    try {
      const res = await apiClient.get(`/meetings/${meetingId}`);
      setMeeting(res.data.data);
    } catch (err) {
      console.error(err);
    }
  };

  React.useEffect(() => { fetchDetails(); }, [meetingId]);

  if (!meeting) return <div className="p-8 text-center">Loading meeting details...</div>;

  return (
    <div className="flex flex-col gap-8">
      <MeetingHeader
        meeting={meeting}
        controls={<MeetingControls meetingId={meetingId} onAction={fetchDetails} />}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 flex flex-col gap-8">
          <Card>
            <h3 className="text-lg font-bold dark:text-white mb-6 flex items-center gap-2">
              <LuActivity className="text-primary-600" /> Live Pipeline Progress
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-8">
              <div className="space-y-6">
                <MeetingProgress stage="Transcription" progress={progress.Transcription || 0} />
                <MeetingProgress stage="Attendance" progress={progress.Attendance || 0} />
              </div>
              <div className="space-y-6">
                <MeetingProgress stage="Notes Generation" progress={progress.Notes || 0} />
                <MeetingProgress stage="Study Pack" progress={progress.StudyPack || 0} />
              </div>
            </div>
          </Card>

          <Card>
            <h3 className="text-lg font-bold dark:text-white mb-6 flex items-center gap-2">
              <LuFileText className="text-primary-600" /> System Logs
            </h3>
            <div className="bg-gray-900 rounded-xl p-4 h-64 overflow-y-auto font-mono text-xs text-green-400 space-y-1">
              {events.length === 0 && <p className="text-gray-600">Waiting for system events...</p>}
              {events.map((ev, i) => (
                <div key={i} className="flex gap-3">
                  <span className="text-gray-500">[{new Date().toLocaleTimeString()}]</span>
                  <span className="text-blue-400">{ev.event}</span>
                  <span>{ev.message}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div className="flex flex-col gap-8">
          <Card>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold dark:text-white">Session Info</h3>
              <MeetingStatus status={meeting.status} />
            </div>
            <div className="space-y-4 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Start Time</span>
                <span className="dark:text-white">{meeting.start_time || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Duration</span>
                <span className="dark:text-white">{meeting.duration || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Storage</span>
                <span className="dark:text-white">1.2 MB</span>
              </div>
            </div>
          </Card>

          <MeetingParticipants participants={[]} />
        </div>
      </div>
    </div>
  );
};

export default MeetingDetailsPage;
