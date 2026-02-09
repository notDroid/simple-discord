import ServerSidebarComponent from "../components/client_server_sidebar";
import { getChatList } from "@/lib/api";

const user_id ='01KGX14KWXN0TR47C3N36N7ZBN';


export default async function ServerSidebarView() {
    const chat_id_list: string[] = await getChatList(user_id).then(res => res.chat_id_list);
    return (
        <ServerSidebarComponent chat_id_list={chat_id_list} />
    );
}