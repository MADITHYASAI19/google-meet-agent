import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';

export const useMeetings = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMeetings = async () => {
    setLoading(true);
    try {
      // In a real scenario, we'd use a paginated list endpoint.
      // For now, we simulate a list or use existing GET /meetings/{id} in a loop if needed,
      // but usually there's a list endpoint. We'll assume /api/v1/meetings exists.
      const response = await apiClient.get('/meetings');
      setMeetings(response.data.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch meetings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  return { meetings, loading, error, refresh: fetchMeetings };
};
