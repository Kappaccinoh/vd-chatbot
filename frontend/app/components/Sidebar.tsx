import { useState } from 'react'
import { History, Network, Plus } from 'lucide-react'

interface SidebarProps {
  onToggleGraph: () => void
}

export default function Sidebar({ onToggleGraph }: SidebarProps) {
  const [conversations, setConversations] = useState([])

  return (
    <div className="w-64 bg-gray-800 p-4 flex flex-col">
      <h1 className="text-xl font-bold text-white mb-4">AI Assistant</h1>
      
      {/* New Chat Button */}
      <button className="bg-blue-500 text-white rounded-lg p-2 mb-4 hover:bg-blue-600 flex items-center justify-center gap-2">
        <Plus size={20} />
        <span>New Chat</span>
      </button>

      {/* Navigation */}
      <nav className="space-y-2">
        <button className="w-full flex items-center space-x-2 text-gray-300 hover:bg-gray-700 p-2 rounded">
          <History size={20} />
          <span>History</span>
        </button>
        <button 
          onClick={onToggleGraph}
          className="w-full flex items-center space-x-2 text-gray-300 hover:bg-gray-700 p-2 rounded"
        >
          <Network size={20} />
          <span>Knowledge Graph</span>
        </button>
      </nav>

      {/* Conversation History */}
      <div className="flex-1 overflow-y-auto mt-4">
        {conversations.map((conv: any) => (
          <div
            key={conv.id}
            className="text-gray-300 hover:bg-gray-700 p-2 rounded cursor-pointer"
          >
            {conv.title}
          </div>
        ))}
      </div>
    </div>
  )
}