import { redirect } from "next/navigation";


export default function DashboardPage() {
	// Temporary redirect to chats page for demo purposes (until dashboard is implemented).
  return (
    <div className="flex items-center justify-center h-screen">
      <h1 className="text-2xl font-bold">Welcome to Harmony!</h1>
    </div>
  );
}

