import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../../api/client';

export const useQuiz = (meetingId) => {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchQuiz = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get(`/quiz/${meetingId}`);
      setQuiz(response.data.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to retrieve quiz');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (meetingId) fetchQuiz();
  }, [meetingId]);

  return { quiz, loading, error, refresh: fetchQuiz };
};
