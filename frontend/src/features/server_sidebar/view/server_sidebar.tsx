import { getMyChatsApiV1UsersMeChatsGet } from "@/lib/api/user/user";
import { UserChatsResponse } from "@/lib/api/model";

import { NetworkError, ApiError } from "@/lib/api/errors";
import ErrorScreen from "@/components/error";

import ServerListWrapper from "../components/sidebar";


export default async function ServerSidebarView( { children }: { children: React.ReactNode } ) {
    let res;
    let chat_id_list: string[] | undefined;
    
    try {
        res = await getMyChatsApiV1UsersMeChatsGet();
        chat_id_list = (res.data as UserChatsResponse).chat_id_list || [];
    } catch (error) {
        if (error instanceof NetworkError) {
            // For network errors, we can treat it as "still loading" since it might be a temporary issue
            chat_id_list = undefined;
        }
        else if (error instanceof ApiError) {
            return <ErrorScreen message={error.message || 'Unable to load chats.'} />;
        }
        else {
            return <ErrorScreen message={'Something went wrong. Please try again later.'} />;
        }
    }

    return (
        <ServerListWrapper initial_chat_id_list={chat_id_list} children={children} />
    );
}