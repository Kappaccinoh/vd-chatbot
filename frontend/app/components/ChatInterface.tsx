'use client'

import { useState, useRef } from 'react'
import { FaMicrophone, FaStop, FaPaperPlane, FaTrash, FaPlay, FaPause } from 'react-icons/fa'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Array<{type: 'user' | 'ai', content: string}>>([])
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const audioRef = useRef<HTMLAudioElement | null>(null)

  const startRecording = async () => {
    try {
      console.log('Requesting microphone access...')
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      console.log('Microphone access granted')

      // Try different MIME types
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : MediaRecorder.isTypeSupported('audio/webm')
          ? 'audio/webm'
          : 'audio/mp4'

      console.log('Using MIME type:', mimeType)
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType,
        audioBitsPerSecond: 128000
      })
      
      chunksRef.current = []
      
      mediaRecorder.ondataavailable = (e) => {
        console.log('Data available:', e.data.size, 'bytes')
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorder.onstop = () => {
        console.log('Recording stopped, processing...')
        const audioBlob = new Blob(chunksRef.current, { type: mimeType })
        console.log('Created blob:', audioBlob.size, 'bytes')
        
        // Clean up old URL if it exists
        if (audioUrl) {
          URL.revokeObjectURL(audioUrl)
        }

        const url = URL.createObjectURL(audioBlob)
        console.log('Created URL:', url)
        
        setAudioBlob(audioBlob)
        setAudioUrl(url)

        // Create a new audio element each time
        const audio = new Audio(url)
        audio.onloadedmetadata = () => {
          console.log('Audio duration:', audio.duration, 'seconds')
        }
        audioRef.current = audio
      }

      mediaRecorderRef.current = mediaRecorder
      mediaRecorder.start(1000) // Record in 1-second chunks
      setIsRecording(true)
      console.log('Recording started')
    } catch (err) {
      console.error('Error accessing microphone:', err)
    }
  }

  const stopRecording = () => {
    console.log('Stopping recording...')
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop()
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
    }
    setIsRecording(false)
  }

  const playAudio = () => {
    if (!audioRef.current) return
    
    console.log('Playing audio...')
    audioRef.current.play()
      .then(() => {
        setIsPlaying(true)
        console.log('Audio playing')
      })
      .catch(err => console.error('Playback error:', err))
  }

  const pauseAudio = () => {
    if (!audioRef.current) return
    
    console.log('Pausing audio...')
    audioRef.current.pause()
    setIsPlaying(false)
  }

  const discardRecording = () => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl)
    }
    setAudioUrl(null)
    setAudioBlob(null)
    setIsPlaying(false)
    audioRef.current = null
  }

  return (
    <div className="flex-1 flex flex-col h-screen bg-gray-800">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] rounded-lg p-3 ${
              message.type === 'user' ? 'bg-blue-500' : 'bg-gray-700'
            }`}>
              {message.content}
            </div>
          </div>
        ))}
      </div>

      {/* Audio Preview */}
      {audioBlob && (
        <div className="p-4 border-t border-gray-700 flex items-center space-x-2">
          <button
            onClick={isPlaying ? pauseAudio : playAudio}
            className="p-2 rounded-full bg-blue-500 hover:opacity-80"
          >
            {isPlaying ? <FaPause /> : <FaPlay />}
          </button>
          <div className="flex-1 text-gray-300 text-sm">
            {audioBlob.size} bytes recorded
          </div>
          <button
            onClick={discardRecording}
            className="p-2 rounded-full bg-red-500 hover:opacity-80"
          >
            <FaTrash />
          </button>
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700">
        <div className="flex items-center space-x-2">
          <button
            onClick={isRecording ? stopRecording : startRecording}
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
            className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none"
            placeholder="Type a message or record audio..."
          />
        </div>
      </div>
    </div>
  )
}