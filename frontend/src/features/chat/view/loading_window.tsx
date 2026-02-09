import LoadingChatPanel from "../ui/chat_loading_panel"
import ChatBar from "../ui/chat_bar"

export default async function LoadingChatWindowView() {
  return (
    <div className="flex h-full w-full flex-col min-w-0">      
        <LoadingChatPanel />
        <ChatBar />
    </div>
  );
}