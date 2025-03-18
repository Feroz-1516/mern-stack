# MERN Stack Blog Application

This project is a full-stack blog application built using a Python backend and React frontend. It demonstrates a microservice architecture with separate frontend and backend components.

## Technology Stack

- Backend: Python (Flask)
- Frontend: React.js
- Database: SQLite (as inferred from the backend code)
- API Documentation: Swagger

## Project Structure

```
mern-stack-converted-7f8d9e2a
├── Dockerfile
├── README.md
├── python-backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── config
│   │   ├── controllers
│   │   ├── models
│   │   └── routes
│   ├── main.py
│   └── requirements.txt
├── react-frontend
│   ├── README.md
│   ├── package.json
│   ├── public
│   └── source
└── tests
    ├── backend
    └── frontend
```

- `python-backend`: Contains the Flask-based Python backend code.
- `react-frontend`: Houses the React.js frontend application.
- `tests`: Includes test files for both backend and frontend.

## Installation

### Backend Setup

1. Navigate to the `python-backend` directory:
   ```
   cd python-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the `react-frontend` directory:
   ```
   cd react-frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

## Running the Application

### Start the Backend Server

1. From the `python-backend` directory, run:
   ```
   python main.py
   ```
   The server will start on `http://localhost:5001`.

### Start the Frontend Development Server

1. From the `react-frontend` directory, run:
   ```
   npm start
   ```
   The React development server will start on `http://localhost:3000`.

## API Documentation

The backend API is documented using Swagger. Once the backend server is running, you can access the Swagger UI at `http://localhost:5001/apidocs/`.

## Testing

### Backend Tests

1. Navigate to the `python-backend` directory.
2. Run the tests using pytest:
   ```
   pytest
   ```

### Frontend Tests

1. Navigate to the `react-frontend` directory.
2. Run the tests using Jest:
   ```
   npm test