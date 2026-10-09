import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const useMeetingWebSocket = (meetingId) => {
  const { user } = useAuth();
  const [status, setStatus] = useState('disconnected');
  const [events, setEvents] = useState([]);
  const [progress, setProgress] = useState({});
  const ws = useRef(null);

  useEffect(() => {
    if (!meetingId || !user) return;

    const token = localStorage.getItem('access_token');
    const socket = new WebSocket(`ws://localhost:8000/ws/meetings/${meetingId}?token=${token}`);

    socket.onopen = () => setStatus('connected');
    socket.onclose = () => setStatus('disconnected');
    socket.onerror = () => setStatus('error');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEvents(prev => [data, ...prev].slice(0, 50));

      if (data.event.includes('Progress')) {
        const key = data.event.replace('Progress', '');
        setProgress(prev => ({ ...prev, [key]: data.progress }));
      }
    };

    ws.current = socket;

    return () => {
      if (socket) socket.close();
    };
  }, [meetingId, user]);

  return { status, events, progress };
};
