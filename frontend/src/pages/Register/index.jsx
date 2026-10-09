import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button, Input, Card } from '../../components/ui/common';
import { LuArrowRight } from 'react-icons/lu';
import AuthLayout from '../../layouts/AuthLayout';

const RegisterPage = () => {
  const { register: authRegister } = useAuth();
  const { register: formRegister, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      await authRegister(data);
      navigate('/login');
    } catch (error) {
      alert('Registration failed');
    }
  };

  return (
    <AuthLayout>
      <Card className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Create Account</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-8">Join the AI Lecture Assistant community</p>

        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
          <Input
            label="Full Name"
            {...formRegister('full_name', { required: 'Name is required' })}
            error={errors.full_name?.message}
          />
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
            Register <LuArrowRight />
          </Button>
        </form>

        <p className="mt-6 text-sm text-gray-500 dark:text-gray-400">
          Already have an account? <Link to="/login" className="text-primary-600 font-semibold">Login</Link>
        </p>
      </Card>
    </AuthLayout>
  );
};

export default RegisterPage;
