'use client'

import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Sidebar from './components/Sidebar'
import KnowledgeGraph from './components/KnowledgeGraph'

export default function Home() {
  const [showGraph, setShowGraph] = useState(false)
  const [graphData, setGraphData] = useState({
    nodes: [
      { id: '1', label: 'Main Topic' },
      { id: '2', label: 'Related Topic 1' },
      { id: '3', label: 'Related Topic 2' },
    ],
    edges: [
      { from: '1', to: '2', label: 'relates to' },
      { from: '1', to: '3', label: 'includes' },
    ]
  })

  const handleToggleGraph = () => {
    setShowGraph(!showGraph)
  }

  return (
    <div className="flex h-screen">
      {/* Left Sidebar */}
      <Sidebar onToggleGraph={handleToggleGraph} />

      {/* Main Chat Area */}
      <div className="flex-1 flex">
        <ChatInterface />
        
        {/* Knowledge Graph Panel */}
        {showGraph && (
          <div className="w-1/3 border-l border-gray-700">
            <KnowledgeGraph data={graphData} />
          </div>
        )}
      </div>
    </div>
  )
}