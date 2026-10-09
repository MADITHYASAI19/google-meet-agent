import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Input } from '../ui/common';
import { useMeetings } from '../../hooks/useMeetings';
import MeetingTable from '../../components/meeting/Table';
import MeetingCard from '../../components/meeting/Card';
import { LuSearch, LuLayoutGrid, LuList } from 'react-icons/lu';

const MeetingsPage = () => {
  const { meetings, loading, error } = useMeetings();
  const navigate = useNavigate();
  const [view, setView] = useState('grid');
  const [search, setSearch] = useState('');

  const filteredMeetings = meetings.filter(m =>
    m.meeting_id.toLowerCase().includes(search.toLowerCase()) ||
    (m.title && m.title.toLowerCase().includes(search.toLowerCase()))
  );

  if (loading) return <div className="p-8 text-center">Loading meetings...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Meetings</h1>
          <p className="text-gray-500 dark:text-gray-400">Manage and monitor your recorded lectures</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <LuSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search meetings..."
              className="pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-dark-card dark:text-white outline-none focus:ring-2 focus:ring-primary-500"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
            <button
              onClick={() => setView('grid')}
              className={`p-2 rounded-md transition-all ${view === 'grid' ? 'bg-white dark:bg-gray-700 shadow-sm' : 'text-gray-500'}`}
            >
              <LuLayoutGrid />
            </button>
            <button
              onClick={() => setView('table')}
              className={`p-2 rounded-md transition-all ${view === 'table' ? 'bg-white dark:bg-gray-700 shadow-sm' : 'text-gray-500'}`}
            >
              <LuList />
            </button>
          </div>
        </div>
      </header>

      {filteredMeetings.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-gray-500">No meetings found matching your search.</p>
        </div>
      ) : view === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredMeetings.map(m => <MeetingCard key={m.meeting_id} meeting={m} onSelect={(id) => navigate(`/meetings/${id}`)} />)}
        </div>
      ) : (
        <MeetingTable meetings={filteredMeetings} onSelect={(id) => navigate(`/meetings/${id}`)} />
      )}
    </div>
  );
};

export default MeetingsPage;
