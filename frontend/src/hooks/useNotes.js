import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../../api/client';

export const useNotes = (meetingId) => {
  const [notes, setNotes] = useState(null);
  const [markdown, setMarkdown] = useState('');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchNotes = async () => {
    setLoading(true);
    try {
      // Fetch JSON notes for metadata and stats
      const notesRes = await apiClient.get(`/notes/${meetingId}`);
      setNotes(notesRes.data.data);

      // Fetch Markdown content
      const mdRes = await apiClient.get(`/notes/${meetingId}/download`);
      setMarkdown(mdRes.data);

      // Note: Statistics are often embedded in notes.json or a separate endpoint
      // We'll assume they are in notes.json or a similar pattern
      setStats(notesRes.data.data.statistics || {});
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to retrieve notes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (meetingId) fetchNotes();
  }, [meetingId]);

  return { notes, markdown, stats, loading, error, refresh: fetchNotes };
};
