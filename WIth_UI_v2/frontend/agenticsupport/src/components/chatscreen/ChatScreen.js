import React from "react";
import { CardContent, Button, TextField, IconButton } from "@mui/material";
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import './chatcss.css';

export default function ChatScreen({ chat, setChat, messages, suggestions, sendMessage, chatContainerRef, setImage, isTyping, }) {
  return (
    <CardContent className="flex flex-col justify-between h-full p-2" style={{ backgroundColor: '#E8F2D8' }}>
      <div class="chat-screen">
        <div className="chat-top-title">Agent Quask</div>
        <div className="chat-log" ref={chatContainerRef}>

          <div>
          {suggestions.length > 0 && (
          <div className="suggestions-content">
            {suggestions.slice(0, 6).map((sug, index) => (
              <div
                key={`sug-${index}`}
                className="message-box robot-message-box"
                onClick={() => setChat(sug)}
              >
                {sug}
              </div>
            ))}
          </div>
        )}


        {messages.map((m, index) => (
          <div key={`msg-${index}`} style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <div className="message-box human-message-box">
                {m.user} 
              </div>
            </div>
            <div style={{ display: "flex", justifyContent: "flex-start" }}>
              <div className="message-box robot-message-box">
              {m.bot === "Agent Quask is typing..." ? (
                  <span className="typing-indicator">
                  <span>Agent Quask is typing</span>
                  <span className="dot dot1">.</span>
                  <span className="dot dot2">.</span>
                  <span className="dot dot3">.</span>
                </span>
              ) : (
                m.bot
              )}
            </div>
            </div>
          </div>
        ))}


        </div>
      </div>


      {!isTyping && (
      <div className="chat-bottom">
        <div className="chat-bottom-text-input">
          <TextField
            size="small"
            value={chat}
            variant="standard"
            onChange={(e) => setChat(e.target.value)}
            placeholder="Ask product related issues..."
            className="flex-grow"
            style={{ width: '13rem' }}
            InputProps={{
              disableUnderline: true,
            }}
          />
        </div>

        <div className="chat-bottom-icon-upload">
          <input
            accept="image/*"
            type="file"
            id="icon-button-file"
            style={{ display: "none" }}
            onChange={(e) => setImage(e.target.files[0])}
          />
          <label htmlFor="icon-button-file">
            <IconButton
              component="span"
              style={{
                color: '#E0F2c4',
                backgroundColor: '#375932',
                borderRadius: '50%',
                width: '48px',
                height: '48px',
                padding: '10px'
              }}
            >
              <PhotoCamera />
            </IconButton>
          </label>
        </div>

        <div>
          <Button
            variant="contained"
            onClick={() => sendMessage()}
            style={{
              color: '#E0F2c4',
              backgroundColor: '#375932',
              borderRadius: '50%',
              width: '48px',
              height: '48px',
              minWidth: '0',
              padding: '0',
            }}
          >
            ▶
          </Button>
        </div>
      </div>
    )}
    </div>
    </CardContent>
  );
}
