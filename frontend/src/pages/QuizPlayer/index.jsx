import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from '../ui/common';
import { useQuiz } from '../../hooks/useQuiz';
import { QuizProgress, QuestionCard } from '../../components/quiz/PlayerComponents';
import { LuChevronLeft, LuChevronRight, LuCheckCircle, LuRotateCcw } from 'react-icons/lu';

const QuizPlayerPage = () => {
  const { meetingId } = useParams();
  const navigate = useNavigate();
  const { quiz, loading, error } = useQuiz(meetingId);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [marked, setMarked] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    if (quiz) {
      // Assume quiz.estimated_time is in minutes
      setTimeLeft((quiz.estimated_time || 15) * 60);
    }
  }, [quiz]);

  useEffect(() => {
    if (timeLeft <= 0) return;
    if (isPaused) return;

    const timer = setInterval(() => {
      setTimeLeft(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, isPaused]);

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const handleAnswer = (val) => {
    setAnswers(prev => ({ ...prev, [currentIndex]: val }));
  };

  const handleToggleMark = () => {
    setMarked(prev => ({ ...prev, [currentIndex]: !prev[currentIndex] }));
  };

  const handleSubmit = async () => {
    if (window.confirm('Are you sure you want to submit the quiz?')) {
      // In a real app, we would POST answers to backend.
      // Here we simulate evaluation.
      navigate(`/quiz/results/${meetingId}`);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading Quiz...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;
  if (!quiz) return <div className="p-8 text-center">No quiz available for this meeting.</div>;

  const questions = quiz.questions || [];
  const currentQuestion = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="flex flex-col gap-8 max-w-5xl mx-auto w-full">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Quiz</h1>
          <p className="text-gray-500 dark:text-gray-400">Meeting: {meetingId.slice(0, 8)}</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-xs text-gray-500 uppercase font-bold">Time Remaining</p>
            <p className={`text-2xl font-mono font-bold ${timeLeft < 60 ? 'text-red-500' : 'dark:text-white'}`}>
              {formatTime(timeLeft)}
            </p>
          </div>
          <Button onClick={() => setIsPaused(!isPaused)} variant="secondary">
            {isPaused ? 'Resume' : 'Pause'}
          </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-3 flex flex-col gap-6">
          <QuizProgress
            total={questions.length}
            current={currentIndex}
            answered={answeredCount}
            marked={Object.keys(marked).length}
          />

          <QuestionCard
            question={currentQuestion}
            currentAnswer={answers[currentIndex]}
            onAnswer={handleAnswer}
            isMarked={marked[currentIndex]}
            onToggleMark={handleToggleMark}
          />

          <div className="flex justify-between items-center">
            <Button
              variant="secondary"
              disabled={currentIndex === 0}
              onClick={() => setCurrentIndex(prev => prev - 1)}
              className="flex items-center gap-2"
            >
              <LuChevronLeft /> Previous
            </Button>

            <Button
              variant="primary"
              onClick={handleSubmit}
              className="bg-green-600 hover:bg-green-700"
            >
              Submit Quiz
            </Button>

            <Button
              variant="secondary"
              disabled={currentIndex === questions.length - 1}
              onClick={() => setCurrentIndex(prev => prev + 1)}
              className="flex items-center gap-2"
            >
              Next <LuChevronRight />
            </Button>
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <Card>
            <h3 className="text-sm font-bold dark:text-white mb-4">Question Map</h3>
            <div className="grid grid-cols-5 gap-2">
              {questions.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentIndex(i)}
                  className={`w-8 h-8 rounded-lg text-xs font-medium transition-all ${
                    currentIndex === i
                      ? 'bg-primary-600 text-white ring-2 ring-primary-300'
                      : answers[i]
                        ? 'bg-green-500 text-white'
                        : marked[i]
                          ? 'bg-orange-500 text-white'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                  }`}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          </Card>

          <Button variant="outline" onClick={() => window.location.reload()} className="flex items-center justify-center gap-2">
            <LuRotateCcw /> Restart Quiz
          </Button>
        </div>
      </div>
    </div>
  );
};

export default QuizPlayerPage;
