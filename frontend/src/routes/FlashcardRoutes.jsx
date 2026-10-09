import React from 'react';
import { Routes, Route } from 'react-router-dom';
import FlashcardsPage from '../pages/Flashcards';
import FlashcardStudyPage from '../pages/FlashcardStudy';

const FlashcardRoutes = () => {
  return (
    <Routes>
      <Route path="/:meetingId" element={<FlashcardsPage />} />
      <Route path="/study/:meetingId" element={<FlashcardStudyPage />} />
    </Routes>
  );
};

export default FlashcardRoutes;
