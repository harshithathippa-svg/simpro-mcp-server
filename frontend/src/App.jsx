import { useState } from "react";
import "./App.css";

function App() {
  const [chats, setChats] = useState([
    {
      id: 1,
      title: "Chat 1",
      messages: [],
    },
  ]);

  const [selectedChat, setSelectedChat] = useState(1);
  const [input, setInput] = useState("");

  const createNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: `Chat ${chats.length + 1}`,
      messages: [],
    };

    setChats([...chats, newChat]);
    setSelectedChat(newChat.id);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    setChats((prev) =>
      prev.map((chat) =>
        chat.id === selectedChat
          ? {
              ...chat,
              messages: [
                ...chat.messages,
                {
                  role: "user",
                  content: userMessage,
                },
              ],
            }
          : chat
      )
    );

    setInput("");

    try {
      const currentChat = chats.find(
        (c) => c.id === selectedChat
      );

      console.log("Sending request...");

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            chat_id: String(selectedChat),
            message: userMessage,
            provider: "openai",
            messages: currentChat?.messages || [],
          }),
        }
      );

      console.log(
        "Response status:",
        response.status
      );

      const data = await response.json();

      console.log("Response data:", data);

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === selectedChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    content: JSON.stringify(
                      data,
                      null,
                      2
                    ),
                  },
                ],
              }
            : chat
        )
      );
    } catch (error) {
      console.error(
        "FETCH ERROR:",
        error
      );

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === selectedChat
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    role: "assistant",
                    content:
                      "ERROR: " +
                      error.message,
                  },
                ],
              }
            : chat
        )
      );
    }
  };

  const currentChat = chats.find(
    (chat) => chat.id === selectedChat
  );

  return (
    <div className="app">
      <div className="sidebar">
        <button
          className="new-chat"
          onClick={createNewChat}
        >
          + New Chat
        </button>

        {chats.map((chat) => (
          <div
            key={chat.id}
            className="chat-item"
            onClick={() =>
              setSelectedChat(chat.id)
            }
          >
            {chat.title}
          </div>
        ))}
      </div>

      <div className="chat-area">
        <h2>{currentChat?.title}</h2>

        <div className="messages">
          {currentChat?.messages.map(
            (msg, index) => (
              <div
                key={index}
                className={`message ${msg.role}`}
              >
                <strong>
                  {msg.role === "user"
                    ? "You: "
                    : "Assistant: "}
                </strong>
                {msg.content}
              </div>
            )
          )}
        </div>

        <div className="input-area">
          <input
            value={input}
            placeholder="Type a message..."
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter")
                sendMessage();
            }}
          />

          <button onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;