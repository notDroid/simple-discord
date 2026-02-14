import { ApiError, NetworkError } from "./errors";
import { getAuthHeader } from "./utils";
import { cache } from 'react';

const API_URL: string = process.env.INTERNAL_API_URL!

// --- Type Definitions ---

export interface ChatMessage {
  chat_id: string;
  ulid: string;
  timestamp: string;
  user_id: string;
  content: string;
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
}

export interface UserChatsResponse {
  chat_id_list: string[];
}

export interface SendMessageRequest {
  content: string;
}

// --- Core Fetch Logic ---

async function fetchErrorWrapper<T>(url: string, options?: RequestInit): Promise<T> {
  let res: Response;

  try {
    res = await fetch(url, options);
  } catch (error) {
    throw new NetworkError('Unable to connect to server');
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

async function secureFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  
  if (!headers.has('Content-Type') && options.method && options.method !== 'GET') {
    headers.set('Content-Type', 'application/json');
  }

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

  // Construct full URL here to centralize logic
  const url = `${API_URL}${endpoint}`;
  
  return await fetchErrorWrapper<T>(url, combinedOptions);
}

// --- API Methods ---

/**
 * GET /chats/{chat_id}
 */
export async function getChatHistory(chat_id: string): Promise<ChatHistoryResponse> {
  return await secureFetch<ChatHistoryResponse>(`/chats/${chat_id}`);
}

/**
 * POST /chats/{chat_id}
 */
export async function sendMessage(chat_id: string, content: string): Promise<ChatMessage> {
  const body: SendMessageRequest = { content };
  
  return await secureFetch<ChatMessage>(`/chats/${chat_id}`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/**
 * GET /users/me/chats
 */
async function _getMyChats(): Promise<UserChatsResponse> {
  return await secureFetch<UserChatsResponse>(`/users/me/chats`);
}

export const getChatList = cache(_getMyChats);