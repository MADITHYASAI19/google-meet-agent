import React from 'react';
import { Card, Badge } from '../../components/ui/common';
import { LuClock, LuBookOpen, LuCpu, LuHardDrive } from 'react-icons/lu';

const StatCard = ({ icon, label, value, color }) => (
  <Card className="flex items-center gap-4">
    <div className={`p-3 rounded-xl ${color} text-white`}>
      {icon}
    </div>
    <div>
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <p className="text-xl font-bold dark:text-white">{value}</p>
    </div>
  </Card>
);

const DashboardPage = () => {
  return (
    <div className="flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Welcome back! 👋</h1>
        <p className="text-gray-500 dark:text-gray-400">Here is what's happening with your lectures.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard icon={<LuClock />} label="Total Minutes" value="1,240" color="bg-blue-500" />
        <StatCard icon={<LuBookOpen />} label="Notes Generated" value="12" color="bg-green-500" />
        <StatCard icon={<LuCpu />} label="AI Credits" value="85%" color="bg-purple-500" />
        <StatCard icon={<LuHardDrive />} label="Storage Used" value="1.2 GB" color="bg-orange-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-2">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold dark:text-white">Recent Meetings</h2>
            <button className="text-sm text-primary-600 font-medium">View All</button>
          </div>
          <div className="flex flex-col gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-xl border border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-600 dark:text-primary-400">
                    L{i}
                  </div>
                  <div>
                    <p className="font-medium dark:text-white">Lecture {i}: Advanced Machine Learning</p>
                    <p className="text-xs text-gray-500">Oct 08, 2026 • 60 mins</p>
                  </div>
                </div>
                <Badge color="success">Completed</Badge>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h2 className="text-xl font-bold dark:text-white mb-6">System Status</h2>
          <div className="flex flex-col gap-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-400">Whisper Model</span>
              <Badge color="success">Active</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-400">LLM Router</span>
              <Badge color="success">Online</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-400">Bot Status</span>
              <Badge color="warning">Idle</Badge>
            </div>
            <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-xl text-center">
              <p className="text-xs text-gray-500 mb-2">Quick Action</p>
              <button className="w-full py-2 bg-primary-600 text-white rounded-lg font-medium text-sm">
                Start New Capture
              </button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
