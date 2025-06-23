# Development Environment Configuration

## Prerequisites
- Docker Desktop installed and running
- VS Code (optional, for dev container support)

## Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
# Copy environment file
cp backend/.env.example backend/.env

# Edit backend/.env with your email configuration
# Then start the development environment
docker-compose -f docker-compose.dev.yml up --build
```

### Option 2: Using Dev Containers
1. Open VS Code in the project root
2. Install "Dev Containers" extension
3. Cmd+Shift+P → "Dev Containers: Reopen in Container"

### Option 3: Manual Setup
```bash
# Frontend
cd frontend
npm install
npm start

# Backend (in separate terminal)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variables
Edit `backend/.env` with your email configuration:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=contact@emptymug.fr
EMAIL_PASSWORD=your_app_password_here
```

## Access Points
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Stopping the Environment
```bash
docker-compose -f docker-compose.dev.yml down
```
