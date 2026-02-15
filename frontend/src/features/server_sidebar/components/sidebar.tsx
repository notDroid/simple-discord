"use client";

import { getMyChatsApiV1UsersMeChatsGet } from "@/lib/api/user/user";
import { UserChatsResponse } from "@/lib/api/model";

import { NetworkError, ApiError } from "@/lib/api/errors";
import ErrorScreen from "@/components/error";
import LoadingScreen from "@/components/loading";
import useSWR from "swr";

import ServerList from "./serverlist";

const fetcher = async (url: string) => {
  const res = await getMyChatsApiV1UsersMeChatsGet()
  const chat_id_list = (res.data as UserChatsResponse).chat_id_list || [];
  return chat_id_list;
};

export default function ServerListWrapper(
  { initial_chat_id_list, children }: 
  { initial_chat_id_list: string[] | undefined, children: React.ReactNode }
) {

  const { data, error, isLoading } = useSWR(
    '/api/user/me/chats', 
    fetcher,
    { 
      fallbackData: initial_chat_id_list, 
      revalidateOnMount: initial_chat_id_list === undefined // Only fetch if we didn't get data from server
    }
  );

  if (!data && error) {
    if (error instanceof NetworkError) {
      return <LoadingScreen />; 
    }
    return <ErrorScreen message={error.message || 'Failed to load server list'} />;
  }

  if (!data && isLoading) {
    return <LoadingScreen />; 
  }
  
  return (
    <div className="fixed flex h-screen w-full">
      <ServerList chat_id_list={data || []} />
      {children}
    </div>
  )
}