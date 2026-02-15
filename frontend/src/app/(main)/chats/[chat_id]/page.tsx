import { use } from 'react';
// import ChatWindowView from "@/features/chat/view/chat_window";


export default function ChatWindow({ params }: { params: Promise<{ chat_id: string }> }) {
  return <div className="h-full w-full flex items-center justify-center">
    <p className="text-app-muted">Chat Window</p>
  </div>;
  // const { chat_id } = use(params);
  // return <ChatWindowView chat_id={chat_id} />;
}