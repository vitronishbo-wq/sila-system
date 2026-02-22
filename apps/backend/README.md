# SILA Backend

Backend service for SILA System built with FastAPI, featuring modular architecture,
authentication, and observability.

## Project Structure

```
backend/
├── modules/              # Modular architecture by domain
│   ├── auth/            # Authentication and authorization
│   ├── citizenship/     # Citizen services
│   ├── commercial/      # Business services
│   └── ...              # Other modules (health, justice, etc.)
├── app/                 # Core application (removed, migrated to modules/)
├── core/                # Core utilities (config, database, logging)
├── tests/               # Unit and integration tests
├── requirements.txt     # Dependencies
└── .github/workflows/   # CI/CD pipelines
```

## Authentication Flow

1. **Login**: POST `/auth/login` with email/password (supports JSON, form, query
   params).
2. **Token Generation**: Returns access_token (JWT) and refresh_token.
3. **2FA (Optional)**: Generates and verifies codes for enhanced security.
4. **Protected Routes**: Use `get_current_active_user` dependency.
5. **Logout**: Revokes tokens via `/auth/logout`.

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL (local or Docker)
- Virtual environment

### 1. Clone and Setup

```bash
git clone <repo-url>
cd sila-system/backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/sila_dev
SECRET_KEY=your-secret-key-here
SENTRY_DSN=your-sentry-dsn  # Optional for error tracking
```

### 4. Database Setup

```bash
alembic upgrade head
```

### 5. Run Tests

```bash
pytest tests/ -v
```

### 6. Start Server

```bash
uvicorn modules.main:app --host 0.0.0.0 --port 8000 --reload
```

## Deployment

- **DEV**: Automated via CI/CD on develop branch.
- **PROD**: Via deploy-prod job with secrets (PROD_SSH_KEY, PROD_HOST, PROD_USER).

## Observability

- **Sentry**: Error tracking integrated.
- **Health Checks**: `/health` endpoint for DB and Redis status.
- **Metrics**: Prometheus endpoints for monitoring.

## Development

- **Modules**: Each module has endpoints, models, schemas, services.
- **Tests**: Run with `pytest` for coverage.
- **CI/CD**: GitHub Actions for tests, deploy, and validation.

For more details, see docs/estrutura_arvore_backend.txt. # Frontend
"frontend/package.json" = @" { "name": "sila-frontend", "version": "0.1.0", "private":
true, "dependencies": { "@testing-library/jest-dom": "^5.14.1",
"@testing-library/react": "^12.0.0", "@testing-library/user-event": "^13.2.1", "axios":
"^0.25.0", "react": "^17.0.2", "react-dom": "^17.0.2", "react-router-dom": "^6.2.1",
"react-scripts": "4.0.3", "web-vitals": "^2.1.0" }, "scripts": { "start": "react-scripts
start", "build": "react-scripts build", "test": "react-scripts test", "eject":
"react-scripts eject" }, "eslintConfig": { "extends": [ "react-app", "react-app/jest" ]
}, "browserslist": { "production": [ ">0.2%", "not dead", "not op_mini all" ],
"development": [ "last 1 chrome version", "last 1 firefox version", "last 1 safari
version" ] } }
