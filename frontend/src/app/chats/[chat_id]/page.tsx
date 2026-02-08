import { use } from 'react';
import ChatWindowView from "@/views/chat/chat_window";


export default function ChatWindow({ params }: { params: Promise<{ chat_id: string }> }) {
  const { chat_id } = use(params);
  return <ChatWindowView chat_id={chat_id} />;
}