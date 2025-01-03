interface MessageProps {
    type: 'user' | 'ai'
    content: string
  }
  
  export default function Message({ type, content }: MessageProps) {
    return (
      <div className={`flex ${type === 'user' ? 'justify-end' : 'justify-start'}`}>
        <div
          className={`max-w-[70%] rounded-lg p-3 ${
            type === 'user'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-700 text-gray-100'
          }`}
        >
          {content}
        </div>
      </div>
    )
  }