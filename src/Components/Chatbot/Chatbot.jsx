import React from 'react'
import { useState } from 'react'
import "./Chatbot.css"

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSendMessage = () => {
    if (input.trim() !== '') {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setInput('');
      // Simulate bot response (replace with actual logic)
      setTimeout(() => {
        setMessages([...messages, { text: input, sender: 'user' }, { text: "Hello there!", sender: 'bot' }]);
      }, 500);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="bg-gray-200 p-4">
        <h1 className="text-lg font-bold">Chatbot</h1>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div key={index} className={`mb-2 ${message.sender === 'user' ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block p-2 rounded-lg ${message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300'}`}>
              {message.text}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4">
        <div className="flex">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded-l-md p-2"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
          />
          <button
            className="bg-blue-500 text-white rounded-r-md p-2"
            onClick={handleSendMessage}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}