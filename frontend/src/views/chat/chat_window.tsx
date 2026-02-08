import ChatHeaderView from "./chat_header";
import ChatPanelView from "./chat_panel";
import ChatBarView from "./chat_bar";

// Temporary constants for demo purposes.
const refreshInterval = 1000;
const user_id ='01KGX14KWXN0TR47C3N36N7ZBN';

export default function ChatWindowView({ chat_id }: { chat_id: string }) {
  return (
    <div className="flex h-full w-full flex-col min-w-0">
      <ChatHeaderView />
      <ChatPanelView chat_id={chat_id} user_id={user_id} refreshInterval={refreshInterval} />
      <ChatBarView chat_id={chat_id} user_id={user_id} />
    </div>
  );
}