import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from '../ui/common';
import { useFlashcards } from '../../hooks/useFlashcards';
import { FlashcardCard, FlashcardControls } from '../../components/flashcards/Card';
import { LuDownload } from 'react-icons/lu';

const FlashcardStudyPage = () => {
  const { meetingId } = useParams();
  const navigate = useNavigate();
  const { cards, metadata, loading, error } = useFlashcards(meetingId);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [favorites, setFavorites] = useState([]);
  const [shuffledCards, setShuffledCards] = useState([]);

  useEffect(() => {
    if (cards && cards.length > 0) {
      setShuffledCards([...cards]);
    }
  }, [cards]);

  const handleShuffle = () => {
    setShuffledCards([...shuffledCards].sort(() => Math.random() - 0.5));
    setCurrentIndex(0);
    setIsFlipped(false);
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setIsFlipped(false);
  };

  const handleToggleFavorite = (id) => {
    setFavorites(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space') { e.preventDefault(); setIsFlipped(prev => !prev); }
      if (e.code === 'ArrowLeft') setCurrentIndex(prev => Math.max(0, prev - 1));
      if (e.code === 'ArrowRight') setCurrentIndex(prev => Math.min(shuffledCards.length - 1, prev + 1));
      if (e.key === 'f' || e.key === 'F') handleToggleFavorite(shuffledCards[currentIndex]?.id);
      if (e.key === 's' || e.key === 'S') handleShuffle();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shuffledCards, currentIndex]);

  if (loading) return <div className="p-8 text-center">Loading Deck...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;
  if (!shuffledCards.length) return <div className="p-8 text-center">No flashcards available for this meeting.</div>;

  const currentCard = shuffledCards[currentIndex];

  return (
    <div className="flex flex-col items-center gap-8 max-w-4xl mx-auto w-full">
      <header className="w-full flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Study Deck</h1>
          <p className="text-gray-500 dark:text-gray-400">Meeting: {meetingId.slice(0, 8)}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => window.open(`/api/v1/flashcards/${meetingId}/download`)} className="flex items-center gap-2">
            <LuDownload /> Export
          </Button>
        </div>
      </header>

      <div className="w-full flex flex-col items-center gap-6">
        <div className="flex justify-between w-full max-w-lg text-sm font-medium text-gray-500">
          <span>Card {currentIndex + 1} of {shuffledCards.length}</span>
          <span>Favorites: {favorites.length}</span>
        </div>

        <div className="w-full flex justify-center">
          <FlashcardCard
            card={currentCard}
            isFlipped={isFlipped}
            onFlip={() => setIsFlipped(!isFlipped)}
          />
        </div>

        <FlashcardControls
          onPrev={() => { setCurrentIndex(prev => Math.max(0, prev - 1)); setIsFlipped(false); }}
          onNext={() => { setCurrentIndex(prev => Math.min(shuffledCards.length - 1, prev + 1)); setIsFlipped(false); }}
          onShuffle={handleShuffle}
          onRestart={handleRestart}
          onToggleFavorite={() => handleToggleFavorite(currentCard.id)}
          isFavorite={favorites.includes(currentCard.id)}
        />

        <div className="w-full max-w-lg h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-primary-600 transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / shuffledCards.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default FlashcardStudyPage;
