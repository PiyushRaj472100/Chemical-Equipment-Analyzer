import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiDownload, FiEye } from 'react-icons/fi';
import './History.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDataset, setSelectedDataset] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/history/`);
      setHistory(response.data.datasets);
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async (datasetId) => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/generate-pdf/${datasetId}/`,
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Failed to generate PDF');
    }
  };

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  return (
    <div className="history-container">
      <h2>Upload History</h2>
      <p>Last 5 uploaded datasets</p>

      {history.length === 0 ? (
        <div className="no-history">
          <p>No upload history yet. Upload your first dataset to get started!</p>
        </div>
      ) : (
        <div className="history-grid">
          {history.map((dataset) => (
            <div key={dataset.id} className="history-card">
              <div className="history-header">
                <h3>{dataset.name}</h3>
                <span className="dataset-id">ID: {dataset.id}</span>
              </div>

              <div className="history-info">
                <div className="info-row">
                  <span>Uploaded:</span>
                  <span>{new Date(dataset.upload_timestamp).toLocaleString()}</span>
                </div>
                <div className="info-row">
                  <span>Total Equipment:</span>
                  <span className="highlight">{dataset.total_equipment}</span>
                </div>
                <div className="info-row">
                  <span>Avg Flowrate:</span>
                  <span>{dataset.average_flowrate.toFixed(2)}</span>
                </div>
                <div className="info-row">
                  <span>Avg Pressure:</span>
                  <span>{dataset.average_pressure.toFixed(2)}</span>
                </div>
                <div className="info-row">
                  <span>Avg Temperature:</span>
                  <span>{dataset.average_temperature.toFixed(2)}</span>
                </div>
              </div>

              <div className="type-distribution">
                <h4>Equipment Types:</h4>
                <div className="type-chips">
                  {Object.entries(dataset.type_distribution).map(([type, count]) => (
                    <span key={type} className="type-chip">
                      {type}: {count}
                    </span>
                  ))}
                </div>
              </div>

              <div className="history-actions">
                <button 
                  className="btn-view"
                  onClick={() => setSelectedDataset(dataset)}
                >
                  <FiEye /> View Details
                </button>
                <button 
                  className="btn-download"
                  onClick={() => downloadPDF(dataset.id)}
                >
                  <FiDownload /> Download PDF
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedDataset && (
        <div className="modal-overlay" onClick={() => setSelectedDataset(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>{selectedDataset.name}</h3>
            <div className="modal-details">
              <p><strong>Dataset ID:</strong> {selectedDataset.id}</p>
              <p><strong>Upload Date:</strong> {new Date(selectedDataset.upload_timestamp).toLocaleString()}</p>
              <p><strong>Total Equipment:</strong> {selectedDataset.total_equipment}</p>
              <p><strong>Average Flowrate:</strong> {selectedDataset.average_flowrate.toFixed(2)}</p>
              <p><strong>Average Pressure:</strong> {selectedDataset.average_pressure.toFixed(2)}</p>
              <p><strong>Average Temperature:</strong> {selectedDataset.average_temperature.toFixed(2)}</p>
              <h4>Type Distribution:</h4>
              {Object.entries(selectedDataset.type_distribution).map(([type, count]) => (
                <p key={type}>{type}: {count}</p>
              ))}
            </div>
            <button onClick={() => setSelectedDataset(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default History;