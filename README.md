#  Data Analytics Agent - Containerized Application

## Workflow Architecture
<img width="521" height="553" alt="image" src="https://github.com/user-attachments/assets/bb2a20d5-4910-46aa-8818-da93fe44d71e" />

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
VITE_BACKEND_URL=http://localhost:8000
LANGSMITH_API_KEY=
LANGGRAPH_API_URL='http://localhost:2024'
```

3. Backend `.env` (Backend-specific configuration):
```bash
PG_USER=postgres
PG_PASS=postgres
PG_HOST=db
PG_PORT=5432
PG_DB=nullaxis
QUERY_TIMEOUT=60
MAX_QUERY_LENGTH=4000
MAX_ROWS_SERVER=5000
DEEPSEEK_API_KEY=
LANGSMITH_API_KEY=
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
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
