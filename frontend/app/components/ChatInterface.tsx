'use client'

import { useState, useRef, useEffect } from 'react'
import { FaMicrophone, FaStop, FaPaperPlane, FaTrash, FaPlay, FaPause } from 'react-icons/fa'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Array<{type: 'user' | 'ai', content: string}>>([])
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [isSending, setIsSending] = useState(false)
  
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
    if (audioRef.current) {
      audioRef.current.play()
      setIsPlaying(true)
    }
  }

  const pauseAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
    }
  }

  const discardRecording = () => {
    setAudioBlob(null)
    setAudioUrl(null)
    setProgress(0)
    setIsPlaying(false)
  }

  useEffect(() => {
    if (!audioRef.current) return

    const updateProgress = () => {
      const audio = audioRef.current
      if (audio) {
        setProgress((audio.currentTime / audio.duration) * 100)
      }
    }

    audioRef.current.addEventListener('timeupdate', updateProgress)
    return () => audioRef.current?.removeEventListener('timeupdate', updateProgress)
  }, [audioUrl])

  const handleSendAudio = async () => {
    if (!audioBlob) return
    setIsSending(true)
  
    try {
      // Create a new File from the Blob with proper MIME type
      const audioFile = new File([audioBlob], 'recording.webm', { 
        type: audioBlob.type 
      })
  
      const formData = new FormData()
      formData.append('audio', audioFile)
  
      // Update the API endpoint URL to match your Django setup
      const response = await fetch('http://localhost:8000/api/voice-input/', {
        method: 'POST',
        body: formData,
        // Add CORS headers
        headers: {
          'Accept': 'application/json',
        },
      })
  
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }
  
      const data = await response.json()
      console.log('Server response:', data)
  
      if (data.transcript) {
        setInput(data.transcript)
        discardRecording()
        // Add the transcribed text to messages
        setMessages(prev => [...prev, { 
          type: 'user', 
          content: data.transcript 
        }])
        
        // If there's an AI response, add it too
        if (data.response) {
          setMessages(prev => [...prev, { 
            type: 'ai', 
            content: data.response 
          }])
        }
      }
    } catch (err) {
      console.error('Error sending audio:', err)
      // You might want to show an error message to the user here
    } finally {
      setIsSending(false)
    }
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

      {/* Audio Preview with Progress Bar */}
      {audioBlob && (
        <div className="p-4 border-t border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <button
              onClick={isPlaying ? pauseAudio : playAudio}
              className="p-2 rounded-full bg-blue-500 hover:opacity-80"
            >
              {isPlaying ? <FaPause /> : <FaPlay />}
            </button>
            
            {/* Progress Bar */}
            <div className="flex-1 bg-gray-700 h-2 rounded-full">
              <div 
                className="bg-blue-500 h-full rounded-full transition-all duration-100"
                style={{ width: `${progress}%` }}
              />
            </div>

            <button
              onClick={handleSendAudio}
              disabled={isSending}
              className={`p-2 rounded-full ${
                isSending ? 'bg-gray-500' : 'bg-green-500 hover:opacity-80'
              }`}
            >
              {isSending ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <FaPaperPlane />
              )}
            </button>
            
            <button
              onClick={discardRecording}
              className="p-2 rounded-full bg-red-500 hover:opacity-80"
            >
              <FaTrash />
            </button>
          </div>

          {/* Time Display */}
          <div className="text-sm text-gray-400 text-center">
            {audioRef.current && !isNaN(audioRef.current.duration) && (
              `${Math.floor(audioRef.current.currentTime)}s / ${Math.floor(audioRef.current.duration)}s`
            )}
          </div>
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