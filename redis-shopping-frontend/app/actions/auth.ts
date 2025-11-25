'use server';

import { redirect } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { setSession, clearSession, getSession } from '@/lib/session';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

export async function loginAction(formData: FormData) {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;

  const validation = loginSchema.safeParse({ email, password });
  
  if (!validation.success) {
    return {
      error: validation.error.errors[0].message,
    };
  }

  try {
    const { token } = await apiClient.login(email, password);
    await setSession(token);
    redirect('/');
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Login failed',
    };
  }
}

export async function logoutAction() {
  await clearSession();
  redirect('/login');
}

export async function getCurrentUser() {
  const token = await getSession();
  
  if (!token) {
    return null;
  }

  try {
    const user = await apiClient.getMe(token);
    return user;
  } catch (error) {
    await clearSession();
    return null;
  }
}
