import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AssignmentPage from '../pages/Assignment';
import AssignmentViewerPage from '../pages/AssignmentViewer';

const AssignmentRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<AssignmentPage />} />
      <Route path="/view/:meetingId" element={<AssignmentViewerPage />} />
    </Routes>
  );
};

export default AssignmentRoutes;
