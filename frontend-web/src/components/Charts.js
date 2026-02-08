import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Charts({ data }) {
  if (!data) return null;

  const { type_distribution, average_values } = data;

  // Equipment Type Distribution Chart
  const typeDistributionData = {
    labels: Object.keys(type_distribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(type_distribution),
        backgroundColor: 'rgba(102, 126, 234, 0.8)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
      },
    ],
  };

  // Average Values Chart
  const averageValuesData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          average_values.flowrate,
          average_values.pressure,
          average_values.temperature,
        ],
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(237, 100, 166, 0.8)',
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(118, 75, 162, 1)',
          'rgba(237, 100, 166, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="charts-section">
      <h2>Data Visualizations</h2>
      <div className="charts-grid">
        <div className="chart-container">
          <h3>Equipment Type Distribution</h3>
          <Bar data={typeDistributionData} options={chartOptions} />
        </div>
        <div className="chart-container">
          <h3>Average Parameters</h3>
          <Bar data={averageValuesData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}

export default Charts;