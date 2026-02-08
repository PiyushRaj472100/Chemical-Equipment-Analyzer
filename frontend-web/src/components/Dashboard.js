import React, { useState } from 'react';
import FileUpload from './FileUpload';
import Summary from './Summary';
import Charts from './Charts';
import DataTable from './DataTable';
import Navbar from './Navbar';
import './Dashboard.css';

function Dashboard() {
  const [summaryData, setSummaryData] = useState(null);
  const [equipmentData, setEquipmentData] = useState([]);

  const handleDataUploaded = (data) => {
    setSummaryData(data.summary);
    setEquipmentData(data.equipment_data);
  };

  return (
    <div className="dashboard">
      <Navbar />
      <div className="dashboard-content">
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          <p>Upload and analyze chemical equipment data</p>
        </div>

        <FileUpload onDataUploaded={handleDataUploaded} />
        
        {summaryData && (
          <>
            <Summary data={summaryData} />
            <Charts data={summaryData} />
            <DataTable data={equipmentData} />
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;