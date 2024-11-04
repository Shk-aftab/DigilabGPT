import React, { useState } from "react";
import "./Chat.css";
import botLogo from "./logo.png";
import axios from "axios";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [input, setInput] = useState("");
  const [currentBotMessage, setCurrentBotMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);

  const prompts = [
    "What is the research about?",
    "What are the key findings?",
    "What methodology was used?",
    "What are the main conclusions?",
  ];

  const sendMessage = async () => {
    if (input.trim() === "") return;
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "user", text: input },
    ]);
    setInput("");
    setShowSuggestions(false);

    setIsTyping(true);

    try {
      const response = await axios.post("http://localhost:8000/query", {
        text: input
      });
      setSources(response.data.sources);
      revealBotMessage(response.data.answer);
    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage = {
        sender: "bot",
        text: "Sorry, I encountered an error while processing your request.",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  const revealBotMessage = (text) => {
    let index = 0;
    setCurrentBotMessage("");

    const intervalId = setInterval(() => {
      setCurrentBotMessage((prev) => prev + text.slice(index, index + 20));
      index += 20;

      if (index >= text.length) {
        clearInterval(intervalId);
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", text: text },
        ]);
        setIsTyping(false);
        setCurrentBotMessage("");
      }
    }, 20);
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
    sendMessage();
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="main-layout">
      <div className="title-header">
        <h2>Research Assistant</h2>
      </div>

      <div className="chat-container">
        {showSuggestions && (
          <div className="chat-suggestions">
            {prompts.map((prompt, index) => (
              <div
                key={index}
                className="suggestion-card"
                onClick={() => handleSuggestionClick(prompt)}
              >
                {prompt}
              </div>
            ))}
          </div>
        )}

        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${
                msg.sender === "user" ? "user-message" : "bot-message"
              }`}
            >
              {msg.sender === "bot" && (
                <img src={botLogo} alt="bot logo" className="bot-logo" />
              )}
              <p>{msg.text}</p>
            </div>
          ))}

          {isTyping && (
            <div className="chat-message bot-message">
              <img src={botLogo} alt="bot logo" className="bot-logo" />
              <p>{currentBotMessage}</p>
            </div>
          )}
        </div>

        <div className="chat-input">
          <input
            type="text"
            placeholder="Type your message here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button onClick={sendMessage}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path
                d="M22 2L11 13"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M22 2L15 22L11 13L2 9L22 2Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
