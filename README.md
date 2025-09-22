#  Data Analytics Agent - Containerized Application

This repository contains a containerized version of the  Data Analytics application, including the frontend, backend, and PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Pratik-A-N/Data-Analytics-Agent.git
   cd NullAxis
   ```

2. Create a `.env` file in the root directory (one has been provided with default values)

3. Build and start the containers:
   ```bash
   docker compose up --build
   ```

This will start:
- Frontend at http://localhost:3000
- Backend API at http://localhost:8000
- PostgreSQL database at localhost:5432

## Services

- **Frontend**: React application served via Nginx
- **Backend**: FastAPI application
- **Database**: PostgreSQL 16

## Environment Setup

The application uses a separated environment configuration structure with three `.env` files:

1. Root `.env` (Database configuration):
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=nullaxis
```

2. Frontend `.env` (Frontend-specific configuration):
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Data Analytics Agent
```

3. Backend `.env` (Backend-specific configuration):
```bash
DEBUG=false
API_PREFIX=/api
HOST=0.0.0.0
PORT=8000
```

### Setting Up Environment Files

1. Copy the example files to create your environment files:
```bash
copy .env.example .env
copy frontend\.env.example frontend\.env
copy backend\.env.example backend\.env
```

2. Modify the values in each `.env` file according to your needs:
   - Root `.env`: Database credentials
   - Frontend `.env`: API URL and frontend settings
   - Backend `.env`: Server configuration and feature flags

**Note**: The `.env` files contain sensitive information and are excluded from version control.

## Development

To rebuild the containers after making changes:
```bash
docker compose down
docker compose up --build
```

To view logs:
```bash
docker compose logs -f
```

To stop the application:
```bash
docker compose down
```

## Data Persistence

PostgreSQL data is persisted in a Docker volume named `postgres_data`. This ensures your data survives container restarts.

To remove all data and start fresh:
```bash
docker compose down -v
```
