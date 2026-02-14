import ServerSidebarComponent from "../components/client_server_sidebar";
import { getChatList } from "@/lib/api";
import { getUserId } from "@/lib/utils";

export default async function ServerSidebarView() {
    const user_id = await getUserId();
    const chat_id_list: string[] = await getChatList(user_id).then(res => res.chat_id_list);
    return (
        <ServerSidebarComponent chat_id_list={chat_id_list} />
    );
}