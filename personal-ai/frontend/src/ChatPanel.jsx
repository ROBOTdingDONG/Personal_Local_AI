// frontend/src/ChatPanel.jsx
// Placeholder content
import React, { useState } from 'react';

function ChatPanel() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMsgEntry = { sender: 'user', text: message };
    setChatHistory(prev => [...prev, userMsgEntry]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      const aiMsgEntry = { sender: 'ai', text: data.answer, citations: data.citations };
      setChatHistory(prev => [...prev, aiMsgEntry]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMsgEntry = { sender: 'ai', text: 'Error communicating with the AI.' };
      setChatHistory(prev => [...prev, errorMsgEntry]);
    }
    setMessage('');
  };

  return (
    <div>
      <h2>Chat</h2>
      <div style={{ height: '300px', border: '1px solid #ccc', overflowY: 'scroll', padding: '10px' }}>
        {chatHistory.map((entry, index) => (
          <div key={index} style={{ marginBottom: '10px', textAlign: entry.sender === 'user' ? 'right' : 'left' }}>
            <strong>{entry.sender === 'user' ? 'You' : 'AI'}:</strong> {entry.text}
            {entry.citations && (
              <div style={{ fontSize: '0.8em', color: 'gray' }}>
                Sources: {JSON.stringify(entry.citations)}
              </div>
            )}
          </div>
        ))}
      </div>
      <input 
        type="text" 
        value={message} 
        onChange={(e) => setMessage(e.target.value)} 
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        style={{ width: 'calc(100% - 60px)', padding: '10px' }}
      />
      <button onClick={handleSend} style={{ padding: '10px' }}>Send</button>
    </div>
  );
}

export default ChatPanel;
