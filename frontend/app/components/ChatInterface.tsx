'use client'

import { useState } from 'react'
import { FaMicrophone, FaStop, FaPaperPlane } from 'react-icons/fa'
import Message from './Message'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Array<{type: 'user' | 'ai', content: string}>>([])
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return

    // Add user message
    setMessages(prev => [...prev, { type: 'user', content: input }])
    
    try {
      const response = await fetch('/api/chat-response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      
      const data = await response.json()
      
      // Add AI response
      setMessages(prev => [...prev, { type: 'ai', content: data.response }])
    } catch (error) {
      console.error('Error:', error)
    }

    setInput('')
  }

  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording and send audio
      setIsRecording(false)
      // Implement stop recording logic
    } else {
      // Start recording
      setIsRecording(true)
      // Implement start recording logic
    }
  }

  return (
    <div className="flex-1 flex flex-col h-screen bg-gray-800">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <Message key={index} type={message.type} content={message.content} />
        ))}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700">
        <div className="flex items-center space-x-2">
          <button
            onClick={toggleRecording}
            className={`p-2 rounded-full ${
              isRecording ? 'bg-red-500' : 'bg-blue-500'
            } hover:opacity-80`}
          >
            {isRecording ? <FaStop /> : <FaMicrophone />}
          </button>
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none"
            placeholder="Type a message..."
          />
          
          <button
            onClick={handleSend}
            className="p-2 bg-blue-500 rounded-full hover:opacity-80"
          >
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  )
}