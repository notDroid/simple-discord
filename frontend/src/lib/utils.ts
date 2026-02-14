import { cookies } from 'next/headers';

export async function getAuthHeader() {
  const cookieStore = await cookies();
  const token = cookieStore.get('session_token')?.value;
  return token ? { Authorization: `Bearer ${token}` } : {};
}