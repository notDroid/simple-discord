const host_name = "walis-macbook-pro";
const API_ENDPOINT = `http://${host_name}:8000/api/v1/`;

export async function getChatHistory(chat_id: string, user_id: string) {
  const res = await fetch(`${API_ENDPOINT}chats/${chat_id}?user_id=${user_id}`);
  if (!res.ok) {
    throw new Error('Failed to fetch chat history');
  }
  const data = await res.json();
  return data.messages;
}

export async function sendMessage(chat_id: string, user_id: string, content: string) {
  const res = await fetch(`${API_ENDPOINT}chats/${chat_id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id, content }),
  });
  if (!res.ok) {
    throw new Error('Failed to send message');
  }
  const data = await res.json();
  return data;
}
