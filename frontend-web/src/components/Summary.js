import React from 'react';

function Summary({ data }) {
  if (!data) return null;

  const { total_equipment, average_values } = data;

  return (
    <div className="summary-section">
      <h2>Summary Statistics</h2>
      <div className="summary-grid">
        <div className="summary-card">
          <h3>Total Equipment</h3>
          <p>{total_equipment}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Flowrate</h3>
          <p>{average_values.flowrate}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Pressure</h3>
          <p>{average_values.pressure}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Temperature</h3>
          <p>{average_values.temperature}</p>
        </div>
      </div>
    </div>
  );
}

export default Summary;