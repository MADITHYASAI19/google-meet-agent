import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MeetingsPage from '../pages/Meetings';
import MeetingDetailsPage from '../pages/MeetingDetails';

const MeetingRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<MeetingsPage />} />
      <Route path="/:meetingId" element={<MeetingDetailsPage />} />
    </Routes>
  );
};

export default MeetingRoutes;
