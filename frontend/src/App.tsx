import { useState } from 'react'
import './App.css'
import FileUpload from './components/FileUpload'
import QueryInput from './components/QueryInput'
import ChatDisplay from './components/ChatDisplay'
import { Toaster } from 'react-hot-toast'
import { TableProvider, useTable } from './context/TableContext';
import { workflowAPI } from './services/workflow.service'
import toast from 'react-hot-toast'

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

const AppContent = () => {
  const { tableId } = useTable();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  return (
    <div className="w-screen h-screen flex flex-col bg-gray-950 p-2">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 2500,
          style: {
            background: '#1f2937',
            color: '#fff',
          },
        }}
      />
      <div className="main-content flex-1 bg-gradient-to-br from-gray-900/80 via-gray-900/90 to-gray-950 rounded-xl border border-gray-800/30 backdrop-blur-xl shadow-2xl relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/[0.01] -z-[1]" />
        <div className="absolute inset-0 bg-gradient-to-t from-gray-950/30 via-transparent to-transparent -z-[1]" />
        <FileUpload />
        <ChatDisplay messages={messages} isProcessing={isProcessing} />
        <QueryInput 
          isProcessing={isProcessing}
          onSubmit={async (query: string) => {
            try {
              if (!tableId) {
                toast.error('Please upload a file first');
                return;
              }

              const userMessage: ChatMessage = {
                id: crypto.randomUUID(),
                type: 'human',
                content: query
              };

              setMessages(prev => [...prev, userMessage]);
              setIsProcessing(true);

              const response = await workflowAPI(query, tableId);
              
              const agentMessage: ChatMessage = {
                id: crypto.randomUUID(),
                type: 'agent',
                content: response.answer,
                visualization: response
              };

              setMessages(prev => [...prev, agentMessage]);
            } catch (error) {
              console.error('Error processing query:', error);
              toast.error('Failed to process query');
              const errorMessage: ChatMessage = {
                id: crypto.randomUUID(),
                type: 'agent',
                content: 'Sorry, there was an error processing your request.'
              };
              setMessages(prev => [...prev, errorMessage]);
            } finally {
              setIsProcessing(false);
            }
          }}
        />
      </div>
    </div>
  );
};

const App = () => {
  return (
    <TableProvider>
      <AppContent />
    </TableProvider>
  );
};

export default App;
