# Flask API Application

A basic Flask API application with example endpoints.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Available Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/hello` - Hello World endpoint

## Testing the API

You can test the API using curl or any API client:

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/hello
``` 