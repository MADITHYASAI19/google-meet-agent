import React from 'react';
import { Card, Button, Input } from '../../components/ui/common';
import { useAuth } from '../../context/AuthContext';

const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-2xl mx-auto flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Profile</h1>
        <p className="text-gray-500 dark:text-gray-400">Manage your account and personal information</p>
      </header>

      <Card className="flex flex-col items-center text-center gap-4">
        <div className="w-24 h-24 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-600 dark:text-primary-400 text-3xl font-bold border-4 border-white dark:border-dark-card">
          {user?.full_name?.charAt(0) || 'U'}
        </div>
        <div>
          <h2 className="text-xl font-bold dark:text-white">{user?.full_name}</h2>
          <p className="text-gray-500 dark:text-gray-400">{user?.email}</p>
          <Badge color="primary">{user?.role}</Badge>
        </div>
      </Card>

      <Card>
        <h3 className="text-lg font-bold dark:text-white mb-6">Security</h3>
        <form className="flex flex-col gap-4 max-w-sm">
          <Input label="Current Password" type="password" />
          <Input label="New Password" type="password" />
          <Input label="Confirm New Password" type="password" />
          <Button className="w-fit">Update Password</Button>
        </form>
      </Card>
    </div>
  );
};

import { Badge } from '../../components/ui/common';
export default ProfilePage;
