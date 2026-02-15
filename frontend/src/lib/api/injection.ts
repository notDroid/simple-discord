import { cookies } from 'next/headers';
import { ApiError, NetworkError } from './errors';

const getBaseUrl = () => {
  return process.env.INTERNAL_API_URL;
};

function injectUrl(url: string): string {
  const baseUrl = getBaseUrl();
  return `${baseUrl}${url}`;
}

async function getAuthHeader() {
  const cookieStore = await cookies();
  const token = cookieStore.get('session_token')?.value;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function injectAuthHeaders(options: RequestInit): Promise<RequestInit> {
  const headers = new Headers(options.headers);
  const authHeaders = await getAuthHeader();

  if (authHeaders) {
    Object.entries(authHeaders).forEach(([key, value]) => {
      if (value) headers.set(key, value as string);
    });
  }

  const combinedOptions: RequestInit = {
    ...options,
    headers
  };
  return combinedOptions;
}

async function fetchErrorWrapper<T>(url: string, options?: RequestInit): Promise<T> {
  let res: Response;

  try {
    res = await fetch(url, options);
  } catch (error) {
    throw new NetworkError(`Unable to connect to server: ${url}:${error}`);
  }

  if (!res.ok) {
    // Attempt to parse validation errors if available
    let errorMessage = `Server error: ${res.statusText}`;
    try {
      const errorBody = await res.json();
      if (errorBody.detail) {
        errorMessage = JSON.stringify(errorBody.detail);
      }
    } catch { /* ignore parsing error */ }
    
    throw new ApiError(res.status, errorMessage);
  }

  return await res.json() as T;
}

export const inject = async <T>(
  url: string,
  options: RequestInit
): Promise<T> => {
  
  url = injectUrl(url);
  options = await injectAuthHeaders(options);

  const data = await fetchErrorWrapper(url, options);

  return data as T;
};