import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function FileUpload({ onDataUploaded }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile);
        setMessage({ text: `Selected: ${selectedFile.name}`, type: 'success' });
      } else {
        setFile(null);
        setMessage({ text: 'Please select a CSV file', type: 'error' });
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage({ text: 'Please select a file first', type: 'error' });
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setMessage({ text: 'Uploading and processing...', type: '' });

    try {
      const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage({ text: 'File uploaded and processed successfully!', type: 'success' });
      onDataUploaded(response.data);
      
      // Reset file input
      setFile(null);
      document.getElementById('file-input').value = '';
      
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Error uploading file';
      setMessage({ text: errorMessage, type: 'error' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-section">
      <h2>Upload CSV File</h2>
      <div className="upload-area">
        <input
          id="file-input"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
        />
        <label htmlFor="file-input" className="upload-label">
          Choose CSV File
        </label>
        <p style={{ marginTop: '15px', color: '#666' }}>
          {file ? `Selected: ${file.name}` : 'No file selected'}
        </p>
        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={!file || uploading}
        >
          {uploading ? 'Uploading...' : 'Upload and Analyze'}
        </button>
      </div>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );
}

export default FileUpload;