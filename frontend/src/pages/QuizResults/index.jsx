import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from '../ui/common';
import { useQuiz } from '../../hooks/useQuiz';
import { LuCheckCircle, LuXCircle, LuTrophy } from 'react-icons/lu';

const QuizResultsPage = () => {
  const { meetingId } = useParams();
  const navigate = useNavigate();
  const { quiz, loading, error } = useQuiz(meetingId);

  if (loading) return <div className="p-8 text-center">Calculating Results...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  // Mocking a score for demonstration as actual evaluation happens on backend
  const score = 75;
  const total = quiz?.questions?.length || 0;

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8">
      <div className="text-center py-10">
        <div className="inline-flex p-4 bg-yellow-100 dark:bg-yellow-900/30 rounded-full text-yellow-600 mb-4">
          <LuTrophy size={48} />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Quiz Completed!</h1>
        <p className="text-gray-500 dark:text-gray-400">Here is how you performed in this lecture.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="text-center p-6">
          <p className="text-sm text-gray-500 mb-1">Total Score</p>
          <p className="text-4xl font-black text-primary-600">{score}%</p>
        </Card>
        <Card className="text-center p-6">
          <p className="text-sm text-gray-500 mb-1">Accuracy</p>
          <p className="text-4xl font-black text-green-500">82%</p>
        </Card>
        <Card className="text-center p-6">
          <p className="text-sm text-gray-500 mb-1">Completion</p>
          <p className="text-4xl font-black text-blue-500">100%</p>
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="text-xl font-bold dark:text-white mb-6">Answer Review</h3>
        <div className="flex flex-col gap-6">
          {quiz?.questions?.map((q, i) => (
            <div key={i} className="p-4 rounded-xl border border-gray-100 dark:border-gray-700">
              <div className="flex justify-between items-start mb-3">
                <p className="font-medium dark:text-white">Q{i+1}: {q.text}</p>
                <Badge color={i % 2 === 0 ? 'success' : 'danger'}>
                  {i % 2 === 0 ? 'Correct' : 'Wrong'}
                </Badge>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div className="p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
                  <p className="text-xs text-gray-400 mb-1">Your Answer</p>
                  <p className="dark:text-white">Option A</p>
                </div>
                <div className="p-3 rounded-lg bg-green-50 dark:bg-green-900/20">
                  <p className="text-xs text-green-600 dark:text-green-400 mb-1">Correct Answer</p>
                  <p className="dark:text-white font-medium">{q.correct_answer || 'Option B'}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
        <Button variant="primary" onClick={() => window.print()}>Download PDF Report</Button>
      </div>
    </div>
  );
};

export default QuizResultsPage;
