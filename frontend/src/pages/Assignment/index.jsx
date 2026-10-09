import React from 'react';
import { Card, Button } from '../ui/common';
import { LuDownload, LuFileText, LuZap } from 'react-icons/lu';
import { useAssignment } from '../../hooks/useAssignment';

const AssignmentPage = ({ meetingId }) => {
  const { assignment, stats, loading, error } = useAssignment(meetingId);

  if (loading) return <div className="p-8 text-center">Loading Assignment...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;
  if (!assignment) return <div className="p-8 text-center">No assignment available.</div>;

  return (
    <div className="flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Assignment Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400">Evaluation and grading for this lecture.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 flex flex-col gap-6">
          <Card className="p-6">
            <h3 className="text-xl font-bold dark:text-white mb-4">Assignment Summary</h3>
            <div className="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-800 rounded-xl">
              <div>
                <p className="text-sm text-gray-500">Title</p>
                <p className="font-bold dark:text-white">{assignment.title || 'Lecture Assignment'}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-500">Total Marks</p>
                <p className="font-bold text-primary-600 text-xl">{assignment.total_marks || '0'}</p>
              </div>
            </div>
          </Card>

          <div className="flex flex-col gap-4">
             <Button
              variant="primary"
              className="py-4 text-lg"
              onClick={() => window.location.href = `/assignment/view/${meetingId}`}
            >
              View Full Assignment
            </Button>
            <Button
              variant="outline"
              className="py-4"
              onClick={() => window.open(`/api/v1/assignment/${meetingId}/download`)}
            >
              Download PDF
            </Button>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <Card className="p-6">
            <h3 className="text-lg font-bold dark:text-white mb-4">Quick Stats</h3>
            <div className="space-y-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Difficulty</span>
                <span className="dark:text-white font-medium">{assignment.difficulty || 'Medium'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Est. Time</span>
                <span className="dark:text-white font-medium">{assignment.estimated_time || '30'} mins</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Questions</span>
                <span className="dark:text-white font-medium">{assignment.total_questions || '0'}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AssignmentPage;
