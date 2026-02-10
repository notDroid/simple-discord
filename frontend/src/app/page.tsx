import { redirect } from "next/navigation";

export default function DashboardPage() {
	// Temporary redirect to chats page for demo purposes (until dashboard is implemented).
  redirect("/chats");
}

