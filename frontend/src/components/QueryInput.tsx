import React, { useState } from 'react';
import { useTable } from '../context/TableContext';

interface QueryInputProps {
  onSubmit: (query: string) => Promise<void>;
  isProcessing?: boolean;
}

const QueryInput: React.FC<QueryInputProps> = ({ onSubmit, isProcessing }) => {
  const { tableId } = useTable();
  const [query, setQuery] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (query.trim() && !isSubmitting) {
      setIsSubmitting(true);
      try {
        await onSubmit(query.trim());
        setQuery('');
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex gap-4 p-4 border-t border-gray-800/30 bg-gray-900/20">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your query here..."
        className="flex-1 bg-gray-900/50 text-gray-200 placeholder-gray-400 rounded-lg px-4 py-3 border border-gray-700/30 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 focus:border-transparent transition-all"
      />
      <button
        onClick={handleSubmit}
        className="min-w-[100px] px-8 py-4 bg-indigo-500/80 hover:bg-indigo-400/80 text-white rounded-full font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-indigo-500/80 backdrop-blur-sm flex items-center justify-center gap-2"
        disabled={!query.trim() || isProcessing}
      >
        <span>Send</span>
      </button>
    </div>
  );
};

export default QueryInput;