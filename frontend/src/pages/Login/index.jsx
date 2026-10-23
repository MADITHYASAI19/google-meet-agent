import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button, Input, Card } from '../../components/ui/common';
import { LuArrowRight } from 'react-icons/lu';

const LoginPage = () => {
  const { register: authRegister, login } = useAuth();
  const { register: formRegister, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      await login(data.email, data.password);
      navigate('/dashboard');
    } catch (error) {
      alert('Invalid credentials');
    }
  };

  return (
    <AuthLayout>
      <Card className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Welcome Back</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-8">Enter your details to access your lectures</p>

        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
          <Input
            label="Email Address"
            type="email"
            {...formRegister('email', { required: 'Email is required' })}
            error={errors.email?.message}
          />
          <Input
            label="Password"
            type="password"
            {...formRegister('password', { required: 'Password is required' })}
            error={errors.password?.message}
          />
          <Button type="submit" className="w-full flex items-center justify-center gap-2">
            Sign In <LuArrowRight />
          </Button>
          <Button type="button" className="w-full flex items-center justify-center gap-2 mt-2 bg-gray-200 dark:bg-gray-700" onClick={async () => {
            try {
              await login('testuser123@example.com', 'password123');
              navigate('/dashboard');
            } catch (e) {
              alert('Temp login failed');
            }
          }}>
            Temp Login
          </Button>
        </form>

        <p className="mt-6 text-sm text-gray-500 dark:text-gray-400">
          Don't have an account? <Link to="/register" className="text-primary-600 font-semibold">Register</Link>
        </p>
      </Card>
    </AuthLayout>
  );
};

import AuthLayout from '../../layouts/AuthLayout';
export default LoginPage;
