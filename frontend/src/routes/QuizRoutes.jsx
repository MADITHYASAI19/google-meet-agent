import React from 'react';
import { Routes, Route } from 'react-router-dom';
import QuizPage from '../pages/Quiz';
import QuizPlayerPage from '../pages/QuizPlayer';
import QuizResultsPage from '../pages/QuizResults';

const QuizRoutes = () => {
  return (
    <Routes>
      <Route path="/:meetingId" element={<QuizPage />} />
      <Route path="/player/:meetingId" element={<QuizPlayerPage />} />
      <Route path="/results/:meetingId" element={<QuizResultsPage />} />
    </Routes>
  );
};

export default QuizRoutes;
