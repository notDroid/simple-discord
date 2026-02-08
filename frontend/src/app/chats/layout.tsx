import ServerSidebar from "@/ui/server_sidebar/server_sidebar";

export default function ChatsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="fixed flex h-screen w-full">
      <ServerSidebar />
      {children}
    </div>
  );
}