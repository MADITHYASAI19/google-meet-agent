import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../../api/client';

export const useAssignment = (meetingId) => {
  const [assignment, setAssignment] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAssignment = async () => {
    setLoading(true);
    try {
      // Main assignment data
      const res = await apiClient.get(`/assignment/${meetingId}`);
      const data = res.data.data;
      setAssignment(data);
      setMetadata(data.metadata || {});
      setStats(data.statistics || {});
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to retrieve assignment');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (meetingId) fetchAssignment();
  }, [meetingId]);

  return { assignment, metadata, stats, loading, error, refresh: fetchAssignment };
};
