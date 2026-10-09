import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NotesPage from '../pages/Notes';
import NotesViewerPage from '../pages/NotesViewer';

const NotesRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<NotesPage />} />
      <Route path="/view/:meetingId" element={<NotesViewerPage />} />
    </Routes>
  );
};

export default NotesRoutes;
