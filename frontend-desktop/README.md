# Chemical Equipment Analyzer - Desktop Application

A desktop application for analyzing chemical equipment data using Tkinter.

## Features

- Upload CSV files containing equipment data
- View equipment summary statistics
- Display detailed equipment data in a table
- Refresh data from the backend API

## Requirements

- Python 3.8+
- Backend API server running on http://localhost:8000

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the backend Django server is running:
```bash
cd backend
python manage.py runserver
```

3. Run the desktop application:
```bash
python main.py
```

## Usage

1. Click "Select CSV File" to upload equipment data
2. View summary statistics in the Equipment Summary section
3. Browse detailed equipment data in the table
4. Use "Refresh Data" to update information from the API

## File Format

CSV files should contain the following columns:
- name: Equipment name
- type: Equipment type
- status: Current status (Active, Maintenance, Standby)
- location: Equipment location
- last_maintenance: Last maintenance date (YYYY-MM-DD)
- next_maintenance: Next maintenance date (YYYY-MM-DD)
