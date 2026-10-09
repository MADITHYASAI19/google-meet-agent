import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import DashboardPage from '../pages/Dashboard';
import ProfilePage from '../pages/Profile';
import SettingsPage from '../pages/Settings';
import LoginPage from '../pages/Login';
import RegisterPage from '../pages/Register';
import DashboardLayout from '../layouts/DashboardLayout';
import AuthLayout from '../layouts/AuthLayout';
import MeetingRoutes from './MeetingRoutes';
import NotesRoutes from './NotesRoutes';
import QuizRoutes from './QuizRoutes';
import FlashcardRoutes from './FlashcardRoutes';
import AssignmentRoutes from './AssignmentRoutes';

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      <Route element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/meetings/*" element={<MeetingRoutes />} />
        <Route path="/notes/*" element={<NotesRoutes />} />
        <Route path="/quiz/*" element={<QuizRoutes />} />
        <Route path="/flashcards/*" element={<FlashcardRoutes />} />
        <Route path="/assignment/*" element={<AssignmentRoutes />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Route>

      <Route path="*" element={<div className="flex items-center justify-center h-screen">404 - Page Not Found</div>} />
    </Routes>
  );
};

export default AppRoutes;
