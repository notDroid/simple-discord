'use client';

import useSWR from 'swr';

// API Functions
import { getChatHistory} from "@/lib/api";

// UI Components
import LoadingChatPanel from "@/ui/chat/chat_loading_panel"
import ErrorChatPanel from "@/ui/chat/chat_error_panel";
import ChatPanel from "@/ui/chat/chat_panel";


export default function ChatPanelView({ chat_id, user_id, refreshInterval }: { chat_id: string, user_id: string, refreshInterval: number }) {
  // 1. SWR Hook: Fetches chat history for the given chat_id and user_id, with auto-refresh every second.
  const { data, error, isLoading } = useSWR(
    chat_id, 
    () => getChatHistory(chat_id, user_id),
    { refreshInterval: refreshInterval }
  )

  
  if (isLoading) return <LoadingChatPanel />;
  if (error) return <ErrorChatPanel />;
  return <ChatPanel messages={data} />;
}