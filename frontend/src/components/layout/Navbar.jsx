import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { LuSun, LuMoon, LuLogOut, LuUser } from 'react-icons/lu';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <nav className="h-16 glass-card sticky top-0 z-50 flex items-center justify-between px-6">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold">AI</div>
        <span className="font-bold text-lg dark:text-white">Lecture Assistant</span>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={() => toggleTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors dark:text-white"
        >
          {theme === 'dark' ? <LuSun /> : <LuMoon />}
        </button>

        {user && (
          <div className="flex items-center gap-3 pl-4 border-l border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-700 dark:text-primary-300 font-medium text-xs">
                {user.full_name?.charAt(0) || 'U'}
              </div>
              <span className="text-sm font-medium dark:text-white">{user.full_name}</span>
            </div>
            <button onClick={logout} className="p-2 text-gray-500 hover:text-red-500 transition-colors">
              <LuLogOut />
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
