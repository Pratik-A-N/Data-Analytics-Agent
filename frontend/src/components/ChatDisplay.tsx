import React, { useEffect, useRef } from 'react';
import Visualization from './Visualization';
import VisualizationWithControls from './VizualizationWithControls';

interface WorkflowResponse {
  answer: string;
  visualization?: string;
  visualization_reason?: string;
  formatted_data_for_visualization?: {
    labels: string[];
    values: Array<{
      data: number[];
      label: string;
    }>;
  };
}

interface ChatMessage {
  id: string;
  type: 'human' | 'agent';
  content: string;
  visualization?: WorkflowResponse;
}

interface ChatDisplayProps {
  messages: ChatMessage[];
  isProcessing?: boolean;
}

const ChatDisplay: React.FC<ChatDisplayProps> = ({ messages, isProcessing }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);
  return (
    <div className="flex-1 overflow-hidden flex flex-col">
      {/* Scrollable message container */}
      <div className="flex-1 overflow-y-auto scroll-smooth px-4" id="message-container">
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className="py-6 first:pt-8 last:pb-8 border-b border-gray-800/40"
            >
              {/* Message header with agent icon */}
              <div className="flex items-center gap-4 mb-4">
                {message.type === 'human' ? (
                  <>
                    <div className="w-8 h-8 rounded-full flex items-center justify-center bg-blue-500/20 text-blue-400 border border-blue-500/30">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path 
                          strokeLinecap="round" 
                          strokeLinejoin="round" 
                          strokeWidth={2} 
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                    </div>
                    <span className="text-sm font-medium text-gray-400">
                      You
                    </span>
                  </>
                ) : (
                  <>
                    <div className="w-8 h-8 rounded-full flex items-center justify-center bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path 
                          strokeLinecap="round" 
                          strokeLinejoin="round" 
                          strokeWidth={2} 
                          d="M13 10V3L4 14h7v7l9-11h-7z"
                        />
                      </svg>
                    </div>
                    <span className="text-sm font-medium text-gray-400">
                      Agent
                    </span>
                  </>
                )}
              </div>

              {/* Message content */}
              <div className="pl-12 text-gray-300 space-y-4 message-content">
                <div className="whitespace-pre-wrap">
                  {message.content}
                </div>
                {message.visualization && message.type === 'agent' && (
                  <div className="mt-4 p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                    <div className="text-sm text-gray-400 mb-2">
                      {message.visualization.visualization_reason}
                    </div>
                    {message.visualization.formatted_data_for_visualization && (
                      <VisualizationWithControls 
                        initialType="bar"
                        data={message.visualization.formatted_data_for_visualization}
                      />
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Loading indicator */}
        {isProcessing && (
          <div className="py-6 border-b border-gray-800/40">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-8 h-8 rounded-full bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin" />
              </div>
              <span className="text-sm font-medium text-gray-400">Processing...</span>
            </div>
            <div className="pl-12 flex gap-2">
              <div className="w-2 h-2 bg-indigo-500/50 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-2 h-2 bg-indigo-500/50 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-2 h-2 bg-indigo-500/50 rounded-full animate-bounce"></div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatDisplay;