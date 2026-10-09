import React from 'react';
import { Card, Button } from '../../components/ui/common';
import { useTheme } from '../../context/ThemeContext';

const SettingsPage = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="max-w-2xl mx-auto flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="text-gray-500 dark:text-gray-400">Configure your application preferences</p>
      </header>

      <Card>
        <h3 className="text-lg font-bold dark:text-white mb-6">Appearance</h3>
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between p-4 rounded-xl border border-gray-100 dark:border-gray-700">
            <div>
              <p className="font-medium dark:text-white">Theme Mode</p>
              <p className="text-xs text-gray-500">Change the visual appearance of the app</p>
            </div>
            <div className="flex gap-2">
              {['light', 'dark', 'system'].map((t) => (
                <button
                  key={t}
                  onClick={() => toggleTheme(t)}
                  className={`px-3 py-1 rounded-lg text-xs capitalize transition-all ${
                    theme === t
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
        </div>
      </Card>

      <Card>
        <h3 className="text-lg font-bold dark:text-white mb-6">Notifications</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 italic">Notifications configuration coming soon...</p>
      </Card>

      <Card>
        <h3 className="text-lg font-bold dark:text-white mb-6">Language</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 italic">Multi-language support coming soon...</p>
      </Card>
    </div>
  );
};

export default SettingsPage;
