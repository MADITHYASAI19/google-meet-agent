import React from 'react';
import { Card, Button, Badge } from '../ui/common';
import { useFlashcards } from '../../hooks/useFlashcards';
import { useNavigate } from 'react-router-dom';
import { LuBookOpen, LuZap, LuClock } from 'react-icons/lu';

const FlashcardsPage = () => {
  const { meetingId } = useParams();
  const navigate = useNavigate();
  const { cards, metadata, loading, error } = useFlashcards(meetingId);

  if (loading) return <div className="p-8 text-center">Loading Deck...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Flashcard Deck</h1>
        <p className="text-gray-500 dark:text-gray-400">Review key concepts from your lecture.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2 p-6">
          <h3 className="text-xl font-bold dark:text-white mb-6">Deck Overview</h3>
          <div className="grid grid-cols-2 gap-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-100 dark:bg-primary-900 text-primary-600 rounded-lg"><LuBookOpen /></div>
              <div>
                <p className="text-xs text-gray-500">Total Cards</p>
                <p className="font-bold dark:text-white">{cards?.length || 0}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 dark:bg-green-900 text-green-600 rounded-lg"><LuZap /></div>
              <div>
                <p className="text-xs text-gray-500">Avg. Difficulty</p>
                <p className="font-bold dark:text-white">{metadata?.difficulty || 'Medium'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 dark:bg-orange-900 text-orange-600 rounded-lg"><LuClock /></div>
              <div>
                <p className="text-xs text-gray-500">Est. Study Time</p>
                <p className="font-bold dark:text-white">{metadata?.est_study_time || '10'} mins</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 dark:bg-purple-900 text-purple-600 rounded-lg"><LuBookOpen /></div>
              <div>
                <p className="text-xs text-gray-500">Model</p>
                <p className="font-bold dark:text-white">{metadata?.model || 'GPT-4'}</p>
              </div>
            </div>
          </div>

          <Button
            className="w-full mt-8 py-4 text-lg"
            onClick={() => navigate(`/flashcards/study/${meetingId}`)}
          >
            Start Studying
          </Button>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-bold dark:text-white mb-4">Quick Tips</h3>
          <ul className="text-sm text-gray-500 dark:text-gray-400 space-y-3">
            <li>• Use <b>Space</b> to flip cards.</li>
            <li>• Use <b>Arrow keys</b> to navigate.</li>
            <li>• Press <b>'F'</b> to mark favorites.</li>
            <li>• Press <b>'S'</b> to shuffle the deck.</li>
          </ul>
        </Card>
      </div>
    </div>
  );
};

import { useParams, useNavigate } from 'react-router-dom';
export default FlashcardsPage;
