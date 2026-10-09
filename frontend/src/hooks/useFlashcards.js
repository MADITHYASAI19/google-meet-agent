import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../../api/client';

export const useFlashcards = (meetingId) => {
  const [cards, setCards] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchFlashcards = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get(`/flashcards/${meetingId}`);
      const data = response.data.data;

      // Assume the response contains cards and metadata
      setCards(data.cards || []);
      setMetadata(data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to retrieve flashcards');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (meetingId) fetchFlashcards();
  }, [meetingId]);

  return { cards, metadata, loading, error, refresh: fetchFlashcards };
};
