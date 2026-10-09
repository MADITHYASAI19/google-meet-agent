import React from 'react';
import { Link } from 'react-router-dom';
import { LuLayoutDashboard, LuMic, LuFileText, LuUsers, LuSettings, LuUser } from 'react-icons/lu';

const Sidebar = () => {
  const menuItems = [
    { icon: <LuLayoutDashboard />, label: 'Dashboard', path: '/dashboard' },
    { icon: <LuMic />, label: 'Meetings', path: '/meetings' },
    { icon: <LuFileText />, label: 'Study Materials', path: '/materials' },
    { icon: <LuUsers />, label: 'Attendance', path: '/attendance' },
    { icon: <LuUser />, label: 'Profile', path: '/profile' },
    { icon: <LuSettings />, label: 'Settings', path: '/settings' },
  ];

  return (
    <aside className="w-64 h-screen glass-card sticky top-16 flex flex-col p-4 gap-2">
      {menuItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:text-primary-600 dark:hover:text-primary-400 transition-all font-medium"
        >
          {item.icon}
          <span>{item.label}</span>
        </Link>
      ))}
    </aside>
  );
};

export default Sidebar;
