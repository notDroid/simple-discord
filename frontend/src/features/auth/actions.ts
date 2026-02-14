'use server'

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

const API_URL = process.env.INTERNAL_API_URL;

export async function loginAction(prevState: any, formData: FormData){
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;

  // 1. Call your FastAPI Backend
  const res = await fetch(`${API_URL}/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password: password }),
  });

  if (!res.ok) {
    return { error: 'Invalid credentials' };
  }

  const data = await res.json();
  const token = data.access_token;

  // 2. Set the Cookie
  // HTTPOnly means JavaScript cannot read it (XSS protection)
  // Secure means HTTPS only (good for prod)
  const cookieStore = await cookies();
  cookieStore.set('session_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 15, // Match your backend (15 mins)
    path: '/',
  });

  // 3. Redirect to dashboard
  redirect('/chats');
}

export async function logoutAction() {
  const cookieStore = await cookies();
  cookieStore.delete('session_token');
  redirect('/login');
}