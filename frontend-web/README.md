# Chemical Equipment Analyzer - Web Application

A React-based web application for analyzing chemical equipment data.

## Features

- Upload CSV files containing equipment data
- View equipment summary statistics
- Display charts and visualizations
- Browse detailed equipment data in a table

## Requirements

- Node.js 14+
- Backend API server running on http://localhost:8000

## Installation

1. Install dependencies:
```bash
npm install
```

2. Ensure the backend Django server is running:
```bash
cd backend
python manage.py runserver
```

3. Start the development server:
```bash
npm start
```

The application will open in your browser at http://localhost:3000

## Usage

1. Use the file upload section to import CSV data
2. View summary statistics in the Equipment Summary section
3. Explore visualizations in the Charts section
4. Browse detailed data in the Data Table section

## File Format

CSV files should contain the following columns:
- name: Equipment name
- type: Equipment type
- status: Current status (Active, Maintenance, Standby)
- location: Equipment location
- last_maintenance: Last maintenance date (YYYY-MM-DD)
- next_maintenance: Next maintenance date (YYYY-MM-DD)

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)
