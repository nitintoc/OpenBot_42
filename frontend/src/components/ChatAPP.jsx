import React, { useState } from 'react';
import { Upload, MessageSquare, FileText, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import Spinner from './ui/spinner';

const ChatApp = () => {
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleFileUpload = async (event) => {
    const formData = new FormData();
    Array.from(event.target.files).forEach(file => {
      formData.append('files', file);
    });

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setUploadStatus(data);
      setFiles(prev => [...prev, ...Array.from(event.target.files)]);
    } catch (error) {
      setUploadStatus({ message: 'Upload failed', error: error.message });
    }
    setLoading(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const query = event.target.query.value;
    if (!query.trim()) return;

    setMessages(prev => [...prev, { type: 'user', content: query }]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { 
        type: 'assistant', 
        content: data.answer,
        sources: data.sources 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        type: 'error', 
        content: 'Failed to get response' 
      }]);
    }
    setLoading(false);
    event.target.query.value = '';
  };

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-4">
      <Card className="shadow-lg">
        <CardHeader className="bg-gray-50 border-b">
          <CardTitle className="text-xl font-semibold text-gray-800">Document Q&A Chat</CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 cursor-pointer border rounded-lg p-2 hover:bg-gray-50 transition-colors">
                <Upload size={20} className="text-gray-600" />
                <span className="text-gray-700">Upload Files</span>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.txt"
                  className="hidden"
                  onChange={handleFileUpload}
                  disabled={loading}
                />
              </label>
              {loading && (
                <div className="flex items-center gap-2 text-gray-600">
                  <Spinner size="sm" />
                  <span>Processing...</span>
                </div>
              )}
            </div>

            {uploadStatus && (
              <Alert variant={uploadStatus.error ? "destructive" : "default"} className="mt-4">
                <AlertDescription>
                  {uploadStatus.message}
                  {uploadStatus.results?.map((result, i) => (
                    <div key={i} className="mt-1 text-sm">
                      {result.filename}: {result.status}
                      {result.message && ` - ${result.message}`}
                    </div>
                  ))}
                </AlertDescription>
              </Alert>
            )}

            <div className="border rounded-lg p-4 h-96 overflow-y-auto space-y-4 bg-white">
              {messages.map((message, index) => (
                <div 
                  key={index} 
                  className={`flex gap-2 ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div className={`max-w-[80%] p-3 rounded-lg ${
                    message.type === 'user' 
                      ? 'bg-blue-500 text-white' 
                      : message.type === 'error'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    <div className="flex items-start gap-2">
                      {message.type === 'user' ? (
                        <MessageSquare size={16} className="mt-1" />
                      ) : message.type === 'error' ? (
                        <AlertCircle size={16} className="mt-1" />
                      ) : (
                        <FileText size={16} className="mt-1" />
                      )}
                      <div>
                        <div className="whitespace-pre-wrap">{message.content}</div>
                        {message.sources && (
                          <div className="text-sm mt-2 text-gray-600">
                            {message.sources}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-3 rounded-lg">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Spinner size="sm" />
                      <span>Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                name="query"
                className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Ask a question about your documents..."
                disabled={loading || files.length === 0}
              />
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                disabled={loading || files.length === 0}
              >
                {loading ? (
                  <>
                    <Spinner size="sm" />
                    <span>Sending...</span>
                  </>
                ) : (
                  'Send'
                )}
              </button>
            </form>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChatApp;