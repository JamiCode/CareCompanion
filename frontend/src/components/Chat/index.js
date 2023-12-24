"use client";
import React, { useEffect, useState, useContext, useCallback } from "react";
import "./index.css";
import { mockChats } from "./mock";
import { useRouter } from "next/router";
import { AuthContext } from "@/components/Auth/AuthProvider";
import useWebSocket, { ReadyState } from "react-use-websocket";

const chart = () => {
  const [messages, setMessages] = useState([]);
  const [scrollInto, setScrollInto] = useState();
  const [inputText, setInputText] = useState("");
  const [isTypingBot, setItTypingBot] = useState(false);

  const authContext = useContext(AuthContext);

  const router = useRouter();
  const { id } = router.query;

  useEffect(() => {
    getMessages();
  }, []);

  useEffect(() => {
    getMessages();
    handleClickChangeSocketUrl(generateSocketUrl());
  }, [id]);

  function handleEnter(event) {
    if (event.key === "Enter") {
      if (inputText) {
        setInputText("");
        handleClickSendMessage(inputText);
        setItTypingBot(true);
      }
    }
  }

  function sendClick() {
    if (inputText) {
      setInputText("");
      handleClickSendMessage(inputText);
      setItTypingBot(true);
    }
  }
  async function getMessages() {
    const response = await fetch(`/api/chat_history/${id}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authContext.token}`,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    setMessageHistory(data);
  }

  useEffect(() => {
    if (scrollInto) {
      document
        .getElementById(`message-${scrollInto}`)
        .scrollIntoView({ behavior: "smooth", block: "start" });
      setScrollInto();
    }
  }, [messages]);

  // Websockets
  const generateSocketUrl = () =>
    `ws://localhost:8000/api/chat/${id}/${authContext.token}`;

  const [socketUrl, setSocketUrl] = useState(generateSocketUrl());
  const [messageHistory, setMessageHistory] = useState([]);
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, {
    onOpen: () => console.log("opened"),

    shouldReconnect: (closeEvent) => true,
  });

  useEffect(() => {
    if (lastMessage !== null) {
      const message = {
        ...JSON.parse(lastMessage.data),
        id: Date.now(),
      };
      setMessageHistory((prev) => prev.concat(message));
      setTimeout(() => {
        document
          .getElementById(`message-${message.id}`)
          .scrollIntoView({ behavior: "smooth", block: "start" });
        setScrollInto();
        setItTypingBot(false);
      }, 0);
    }
  }, [lastMessage, setMessageHistory]);

  const handleClickChangeSocketUrl = useCallback(
    (newUrl) => setSocketUrl(newUrl),
    []
  );

  const handleClickSendMessage = useCallback((text) => sendMessage(text), []);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };
  return (
    <div className="flex-1 p:2 sm:p-6 justify-between flex flex-col h-full">
      <div
        id="messages"
        className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch"
      >
        {messageHistory.map((message) => {
          return (
            <div
              className="chat-message"
              id={"message-" + message.id}
              key={message.id}
            >
              <div
                className={
                  "flex items-end " +
                  (message.is_bot_message ? "justify-end" : "")
                }
              >
                <div className="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-2 items-start">
                  <div>
                    <span
                      className={
                        "px-4 py-2 rounded-lg inline-block rounded-bl-none text-gray-600 " +
                        (message.is_bot_message ? "bg-blue-600" : "bg-gray-300")
                      }
                    >
                      {message.text_content}
                    </span>
                  </div>
                </div>
                <img
                  src="https://images.unsplash.com/photo-1549078642-b2ba4bda0cdb?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144"
                  alt="My profile"
                  className="w-6 h-6 rounded-full order-1"
                />
              </div>
            </div>
          );
        })}
        {isTypingBot ? "......." : ""}
      </div>

      <div className="border-t-2 border-gray-200 px-4 pt-4 mb-2 sm:mb-0">
        <div className="relative flex">
          <span className="absolute inset-y-0 flex items-center">
            <button
              type="button"
              className="inline-flex items-center justify-center rounded-full h-12 w-12 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="h-6 w-6 text-gray-600"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                ></path>
              </svg>
            </button>
          </span>

          <input
            value={inputText}
            onChange={handleInputChange}
            type="text"
            placeholder="Write your message!"
            className="w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-12 bg-gray-200 rounded-md py-3"
            onKeyDown={handleEnter}
          />

          <div className="absolute right-0 items-center inset-y-0 hidden sm:flex">
            <button
              type="button"
              className="inline-flex items-center justify-center rounded-full h-10 w-10 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="h-6 w-6 text-gray-600"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                ></path>
              </svg>
            </button>

            <button
              type="button"
              className="inline-flex items-center justify-center rounded-full h-10 w-10 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="h-6 w-6 text-gray-600"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                ></path>
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                ></path>
              </svg>
            </button>

            <button
              type="button"
              className="inline-flex items-center justify-center rounded-full h-10 w-10 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="h-6 w-6 text-gray-600"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </button>
            <button
              onClick={sendClick}
              type="button"
              className="inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-white bg-blue-500 hover:bg-blue-400 focus:outline-none"
            >
              <span className="font-bold">Send</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="h-6 w-6 ml-2 transform rotate-90"
              >
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default chart;
