import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { LuArrowLeft, LuArrowRight, LuShuffle, LuStar, LuRotateCcw } from 'react-icons/lu';

const FlashcardCard = ({ card, isFlipped, onFlip }) => {
  return (
    <div
      className="relative w-full max-w-lg h-80 cursor-pointer perspective-1000"
      onClick={onFlip}
    >
      <motion.div
        className="w-full h-full transition-all duration-500 preserve-3d"
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ type: 'spring', stiffness: 260, damping: 20 }}
      >
        {/* Front */}
        <div className="absolute inset-0 w-full h-full backface-hidden glass-card rounded-3xl p-8 flex flex-col items-center justify-center text-center">
          <span className="text-xs font-bold text-primary-600 uppercase mb-4">Question</span>
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white leading-relaxed">
            {card.question}
          </h3>
          <p className="mt-8 text-sm text-gray-400 animate-pulse">Click to flip</p>
        </div>

        {/* Back */}
        <div
          className="absolute inset-0 w-full h-full backface-hidden rotate-y-180 glass-card rounded-3xl p-8 flex flex-col items-center justify-center text-center bg-primary-50 dark:bg-primary-900/20"
        >
          <span className="text-xs font-bold text-primary-600 uppercase mb-4">Answer</span>
          <p className="text-xl text-gray-800 dark:text-gray-200 leading-relaxed">
            {card.answer}
          </p>
          <p className="mt-8 text-sm text-gray-400 animate-pulse">Click to flip back</p>
        </div>
      </motion.div>
    </div>
  );
};

export const FlashcardControls = ({ onPrev, onNext, onShuffle, onRestart, onToggleFavorite, isFavorite }) => (
  <div className="flex flex-wrap items-center justify-center gap-4 mt-8">
    <Button variant="secondary" onClick={onPrev} className="flex items-center gap-2">
      <LuArrowLeft /> Prev
    </Button>
    <Button variant="outline" onClick={onToggleFavorite} className={`flex items-center gap-2 ${isFavorite ? 'text-yellow-500 border-yellow-500' : ''}`}>
      <LuStar /> Favorite
    </Button>
    <Button variant="secondary" onClick={onNext} className="flex items-center gap-2">
      Next <LuArrowRight />
    </Button>
    <div className="flex gap-2 ml-4">
      <Button variant="outline" onClick={onShuffle} title="Shuffle Deck">
        <LuShuffle />
      </Button>
      <Button variant="outline" onClick={onRestart} title="Restart Deck">
        <LuRotateCcw />
      </Button>
    </div>
  </div>
);

export { FlashcardCard, FlashcardControls };
