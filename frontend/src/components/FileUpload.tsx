import React, { type ChangeEvent, useState } from 'react';
import { ingestService } from '../services/ingest.service';
import toast from 'react-hot-toast';
import { useTable } from '../context/TableContext';

interface UploadedFile {
  name: string;
  rows: number;
}

const FileUpload: React.FC = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const { setTableId } = useTable();

  const handleFileUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'text/csv') {
      setIsUploading(true);
      try {
        const result = await ingestService.uploadFile(file);
        // const result = {
        //     table_name: 'Data_Set_t_311_Service_Requests_from_2010_to_Present',
        //     rows_loaded: 1000
        // }
        setUploadedFile({
          name: file.name,
          rows: result.rows_loaded
        });
        console.log('Upload result:', result);
        setTableId(result.table_name);
        toast.success(`Successfully uploaded ${file.name}`, {
          duration: 2500,
        });
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Upload failed';
        toast.error(errorMessage, {
          duration: 2500,
        });
        console.error('Upload error:', err);
      } finally {
        setIsUploading(false);
      }
    } else {
      toast.error('Please upload a CSV file', {
        duration: 2500,
      });
    }
  };

  const handleReset = () => {
    setUploadedFile(null);
    setTableId(null);
  };

  return (
    <div className="flex flex-col items-center gap-2 p-4 border-b border-gray-800/30">
      {!uploadedFile ? (
        <label 
          htmlFor="csv-upload" 
          className={`min-w-[140px] px-6 py-2.5 ${
            isUploading 
              ? 'bg-gray-700/80 cursor-wait' 
              : 'bg-gray-900/80 hover:bg-gray-800/80 cursor-pointer'
          } text-white rounded-full font-medium transition-all duration-200 backdrop-blur-md border border-gray-700/50 shadow-xl shadow-black/20 flex items-center justify-center gap-2`}
        >
          {isUploading ? (
            <svg 
              className="w-5 h-5 animate-spin" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg 
              className="w-5 h-5" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24" 
              xmlns="http://www.w3.org/2000/svg"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          )}
          <span>{isUploading ? 'Uploading...' : 'Upload CSV'}</span>
        </label>
      ) : (
        <div className="flex items-center gap-3 px-6 py-2.5 bg-green-900/20 text-white rounded-xl border border-green-500/20">
          <svg 
            className="w-5 h-5 text-green-500" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div className="flex flex-col">
            <span className="text-sm font-medium">{uploadedFile.name}</span>
            <span className="text-xs text-gray-400">{uploadedFile.rows} rows loaded</span>
          </div>
          <button
            onClick={handleReset}
            className="ml-2 p-1 hover:bg-gray-700/50 rounded-full transition-colors"
          >
            <svg 
              className="w-4 h-4" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      )}
      <input
        type="file"
        id="csv-upload"
        accept=".csv"
        onChange={handleFileUpload}
        className="hidden"
      />
      
    </div>
  );
};

export default FileUpload;