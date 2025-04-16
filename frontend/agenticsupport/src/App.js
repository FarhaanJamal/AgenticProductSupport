import React, { useState, useEffect, useRef } from "react";
import { Card } from "@mui/material";
import HomeScreen from './components/homescreen/HomeScreen';
import ChatScreen from './components/chatscreen/ChatScreen';
import './index.css';

export default function ChatbotApp() {
  const [step, setStep] = useState(1);
  const [image, setImage] = useState(null);
  const [chat, setChat] = useState("");
  const [messages, setMessages] = useState([]);
  const isTyping = messages.length > 0 && messages[messages.length - 1]?.bot === "Agent Quask is typing...";
  const [suggestions, setSuggestions] = useState([]);
  const chatContainerRef = useRef(null);

  const handleQRImageCapture = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("http://127.0.0.1:5001/upload_qr_image", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    setSuggestions(data.suggestions || []);
    setStep(2);
  };

const sendMessage = async (selectedMessage = null) => {
  const messageToSend = selectedMessage || chat;
  if (!messageToSend.trim()) return;

  // Add user's message and a typing placeholder for the bot
  setMessages(prev => [
    ...prev,
    { user: messageToSend, bot: "Agent Quask is typing..." }
  ]);
  setChat(""); 

  const data = new FormData();
  data.append("message", messageToSend);
  if (image) data.append("file", image);

  const res = await fetch("http://127.0.0.1:5001/chat", {
    method: "POST",
    body: data,
  });

  const replyData = await res.json();

  // Replace the last "typing..." bot message with the real response
  setMessages(prev => {
    const newMessages = [...prev];
    newMessages[newMessages.length - 1] = {
      user: messageToSend,
      bot: replyData.message
    };
    return newMessages;
  });

  setSuggestions(replyData.suggestions || []);
  setStep(2);
};

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex items-center justify-center min-h-screen" style={{ backgroundColor: '#CBAEF2' }}>
      <Card className="w-[375px] h-[667px] flex flex-col shadow-2xl rounded-3xl overflow-hidden">
        {step === 1 ? (
          <HomeScreen handleQRImageCapture={handleQRImageCapture} />
        ) : (
          <ChatScreen
            chat={chat}
            setChat={setChat}
            messages={messages}
            suggestions={suggestions}
            sendMessage={sendMessage}
            chatContainerRef={chatContainerRef}
            setImage={setImage}
            isTyping={isTyping}
          />
        )}
      </Card>
    </div>
  );
}
