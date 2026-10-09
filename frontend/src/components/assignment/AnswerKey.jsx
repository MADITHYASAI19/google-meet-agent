import React, { useState } from 'react';
import { Card, Button } from '../ui/common';
import { LuEye, LuEyeOff } from 'react-icons/lu';

const AssignmentAnswerKey = ({ answerKey }) => {
  const [showAnswers, setShowAnswers] = useState(false);

  if (!answerKey) return null;

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold dark:text-white">Answer Key</h3>
        <Button
          variant="secondary"
          onClick={() => setShowAnswers(!showAnswers)}
          className="flex items-center gap-2"
        >
          {showAnswers ? <LuEyeOff /> : <LuEye />}
          {showAnswers ? 'Hide Answers' : 'Show Answers'}
        </Button>
      </div>

      {showAnswers && (
        <div className="flex flex-col gap-6">
          {answerKey.answers?.map((ans, i) => (
            <div key={i} className="p-4 rounded-xl bg-green-50 dark:bg-green-900/10 border border-green-100 dark:border-green-900/30">
              <div className="flex items-center gap-2 mb-2">
                <span className="font-bold text-green-600">Q{i+1}:</span>
                <span className="text-sm font-medium dark:text-white">Correct Answer</span>
              </div>
              <p className="text-gray-800 dark:text-gray-200 mb-3">{ans.correct_answer}</p>
              {ans.explanation && (
                <div className="text-xs text-gray-500 dark:text-gray-400 p-2 bg-white dark:bg-dark-card rounded border border-gray-100 dark:border-gray-700">
                  <strong>Explanation:</strong> {ans.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};

export default AssignmentAnswerKey;
