'use client'

import { useEffect, useRef } from 'react'
import { Edge, Network, Node } from 'vis-network'
import { DataSet } from 'vis-data'


interface KnowledgeGraphProps {
  data?: {
    nodes: Array<{ id: string; label: string }>
    edges: Array<{ from: string; to: string; label?: string }>
  }
}

export default function KnowledgeGraph({ data }: KnowledgeGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current || !data) return

    // Default data if none provided
    const graphData = data || {
      nodes: [
        { id: '1', label: 'Topic 1' },
        { id: '2', label: 'Topic 2' },
      ],
      edges: [
        { from: '1', to: '2', label: 'relates to' }
      ]
    }

    // Create the graph
    const nodes = new DataSet<Node>(graphData.nodes)
    const edges = new DataSet<Edge>(graphData.edges)

    const options = {
      nodes: {
        shape: 'dot',
        size: 16,
        font: {
          size: 14,
          color: '#ffffff'
        },
        borderWidth: 2,
        color: {
          background: '#4299e1',
          border: '#2b6cb0',
          highlight: {
            background: '#2b6cb0',
            border: '#2c5282'
          }
        }
      },
      edges: {
        color: {
          color: '#718096',
          highlight: '#4a5568'
        },
        font: {
          color: '#ffffff',
          size: 12
        },
        width: 2
      },
      physics: {
        enabled: true,
        stabilization: {
          iterations: 100
        }
      }
    }

    const network = new Network(
      containerRef.current,
      { nodes, edges },
      options
    )

    return () => {
      network.destroy()
    }
  }, [data])

  return (
    <div className="h-full bg-gray-800 p-4">
      <h2 className="text-white text-lg font-semibold mb-4">Knowledge Graph</h2>
      <div ref={containerRef} className="h-[calc(100%-2rem)]" />
    </div>
  )
}