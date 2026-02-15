import ServerSidebarView from "@/features/server_sidebar/view/server_sidebar";

export default function ChatsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ServerSidebarView children={children} />
  );
}