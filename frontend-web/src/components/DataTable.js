import React from 'react';

function DataTable({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="table-section">
      <h2>Equipment Data Table</h2>
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{item['Equipment Name']}</td>
                <td>{item.Type}</td>
                <td>{item.Flowrate}</td>
                <td>{item.Pressure}</td>
                <td>{item.Temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataTable;