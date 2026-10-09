import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Button } from '../ui/common';
import { useAssignment } from '../../hooks/useAssignment';
import AssignmentToolbar from '../../components/assignment/Toolbar';
import AssignmentHeader from '../../components/assignment/Header';
import AssignmentQuestion from '../../components/assignment/Question';
import AssignmentRubric from '../../components/assignment/Rubric';
import AssignmentAnswerKey from '../../components/assignment/AnswerKey';
import AssignmentStatistics from '../../components/assignment/Statistics';
import { LuArrowLeft } from 'react-icons/lu';

const AssignmentViewerPage = () => {
  const { meetingId } = useParams();
  const { assignment, stats, loading, error } = useAssignment(meetingId);
  const [search, setSearch] = useState('');

  if (loading) return <div className="p-8 text-center">Loading Assignment...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;
  if (!assignment) return <div className="p-8 text-center">Assignment not found.</div>;

  const filteredQuestions = (assignment.questions || []).filter(q =>
    q.text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <button
          onClick={() => window.history.back()}
          className="flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 transition-colors"
        >
          <LuArrowLeft /> Back to Dashboard
        </button>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => window.print()}>Print PDF</Button>
        </div>
      </div>

      <AssignmentHeader assignment={assignment} />

      <div className="flex flex-col lg:flex-row gap-8">
        <div className="flex-1 flex flex-col gap-6">
          <AssignmentToolbar
            onSearch={setSearch}
            onDownload={() => window.open(`/api/v1/assignment/${meetingId}/download`)}
            onCopy={() => alert('Content copied to clipboard!')}
            onPrint={() => window.print()}
          />

          <div className="flex flex-col gap-4">
            {filteredQuestions.map((q, i) => (
              <AssignmentQuestion key={i} index={i} question={q} />
            ))}
            {filteredQuestions.length === 0 && (
              <div className="p-12 text-center text-gray-500">No questions match your search.</div>
            )}
          </div>

          <AssignmentRubric rubric={assignment.rubric} />
          <AssignmentAnswerKey answerKey={assignment.answer_key} />
        </div>

        <div className="w-full lg:w-80 flex flex-col gap-6">
          <AssignmentStatistics stats={stats} />
          <Card className="p-6">
            <h4 className="text-sm font-bold dark:text-white mb-4">Assignment Metadata</h4>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">Model</span>
                <span className="dark:text-white">{assignment.model || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Provider</span>
                <span className="dark:text-white">{assignment.provider || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Prompt Version</span>
                <span className="dark:text-white">{assignment.prompt_version || '1.0'}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AssignmentViewerPage;
