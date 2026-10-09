import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from '../ui/common';
import { useNotes } from '../../hooks/useNotes';
import NotesToolbar from '../notes/Toolbar';
import NotesViewer from '../notes/Viewer';
import { NotesStatistics, NotesMetadata } from '../notes/Info';
import { LuArrowLeft, LuDownload } from 'react-icons/lu';

const NotesViewerPage = () => {
  const { meetingId } = useParams();
  const navigate = useNavigate();
  const { notes, markdown, stats, loading, error, refresh } = useNotes(meetingId);
  const [search, setSearch] = useState('');

  const handleDownload = async (format) => {
    const url = format === 'md'
      ? `/api/v1/notes/${meetingId}/download`
      : `/api/v1/notes/${meetingId}`;
    window.open(url, '_blank');
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-screen gap-4">
      <div className="w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-500">Processing AI Notes...</p>
    </div>
  );

  if (error) return (
    <div className="p-8 text-center">
      <h2 className="text-xl font-bold text-red-500 mb-4">Notes Not Available</h2>
      <p className="text-gray-500 mb-6">{error}</p>
      <Button onClick={() => navigate('/meetings')}>Back to Meetings</Button>
    </div>
  );

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 transition-colors"
        >
          <LuArrowLeft /> Back to Meeting
        </button>
        <div className="flex gap-2">
          <Badge color="success">Generated</Badge>
          <span className="text-xs text-gray-400 self-center">{notes?.created_at || ''}</span>
        </div>
      </div>

      <div className="flex flex-col gap-6">
        <NotesStatistics stats={stats} />

        <div className="flex flex-col lg:flex-row gap-6">
          <div className="flex-1 flex flex-col gap-4">
            <NotesToolbar
              onSearch={setSearch}
              onDownload={handleDownload}
              onCopy={() => {
                navigator.clipboard.writeText(markdown);
                alert('Copied to clipboard!');
              }}
              onPrint={() => window.print()}
            />
            <NotesViewer content={markdown} search={search} />
          </div>

          <div className="w-full lg:w-80 flex flex-col gap-6">
            <NotesMetadata metadata={notes} />
            <Card>
              <h4 className="text-sm font-bold dark:text-white mb-4">Reading Guide</h4>
              <div className="text-xs text-gray-500 space-y-2">
                <p>• Focus on bolded terms for key concepts.</p>
                <p>• Use the search bar to find specific topics.</p>
                <p>• Export to Markdown for your personal knowledge base.</p>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotesViewerPage;
