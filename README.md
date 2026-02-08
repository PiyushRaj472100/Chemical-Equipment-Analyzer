# Chemical Equipment Analyzer (CEP)

A comprehensive system for analyzing and managing chemical equipment data with both web and desktop interfaces.

## Project Structure

```
├── backend/
│   ├── chemical_analyzer/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   ├── manage.py
│   └── requirements.txt
├── frontend-web/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── Summary.js
│   │   │   ├── Charts.js
│   │   │   └── DataTable.js
│   ├── package.json
│   └── README.md
├── frontend-desktop/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── sample_data/
│   └── equipment_data.csv
└── README.md
```

## Features

- **Backend API**: Django REST API for data management
- **Web Interface**: React-based web application
- **Desktop Application**: Tkinter-based desktop client
- **CSV Upload**: Import equipment data from CSV files
- **Data Visualization**: Charts and summary statistics
- **Equipment Tracking**: Monitor maintenance schedules and equipment status

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the Django server:
```bash
python manage.py runserver
```

The API will be available at http://localhost:8000

### Web Frontend Setup

1. Navigate to the frontend-web directory:
```bash
cd frontend-web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The web application will be available at http://localhost:3000

### Desktop Application Setup

1. Navigate to the frontend-desktop directory:
```bash
cd frontend-desktop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the desktop application:
```bash
python main.py
```

## Sample Data

A sample CSV file is provided in `sample_data/equipment_data.csv` with 20 equipment records. You can use this file to test the upload functionality.

## API Endpoints

- `GET /api/equipment/` - List all equipment
- `POST /api/upload/` - Upload CSV file
- `GET /api/summary/` - Get equipment summary statistics
- `GET /admin/` - Django admin interface

## CSV File Format

When uploading CSV files, ensure they contain the following columns:
- `name`: Equipment name
- `type`: Equipment type
- `status`: Current status (Active, Maintenance, Standby)
- `location`: Equipment location
- `last_maintenance`: Last maintenance date (YYYY-MM-DD)
- `next_maintenance`: Next maintenance date (YYYY-MM-DD)

## Technology Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.1
- Pandas 2.1.3

### Web Frontend
- React 18.2.0
- React Scripts 5.0.1
- Axios 1.6.0
- Recharts 2.8.0

### Desktop Application
- Python Tkinter
- Requests 2.31.0
- Pandas 2.1.3

## Development

### Adding New Features

1. **Backend**: Add new models, views, and serializers in the `backend/api/` directory
2. **Web Frontend**: Create new React components in `frontend-web/src/components/`
3. **Desktop**: Update the Tkinter interface in `frontend-desktop/main.py`

### Database Management

- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Access admin: http://localhost:8000/admin/

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
