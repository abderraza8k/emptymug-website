# EmptyMug Website

[![Build and Publish](https://github.com/abderraza8k/emptymug-project/actions/workflows/build-and-publish.yml/badge.svg)](https://github.com/abderraza8k/emptymug-project/actions/workflows/build-and-publish.yml)

A modern, responsive website for EmptyMug built with React and Python FastAPI, featuring a sleek Apple-inspired design with smooth animations, database storage, and AI-powered content moderation.

## 🚀 Features

- **Modern Design**: Apple-inspired UI with clean aesthetics
- **Interactive Background**: Subtle animated Voronoi diagram
- **Responsive**: Works perfectly on all devices
- **Smooth Animations**: Subtle animations powered by Framer Motion
- **Advanced Contact Form**: Enhanced validation with country code selection
- **Database Storage**: Multi-database support (In-memory, PostgreSQL, DynamoDB)
- **AI Content Moderation**: Ollama LLM integration for content filtering
- **Enhanced Validation**: Email format, phone number, and input validation
- **TypeScript**: Full TypeScript support for better development experience
- **Dev Containers**: Ready-to-use development environment
- **Docker Ready**: Production-ready Docker containers with automated builds
- **CI/CD**: GitHub Actions for automated testing, building, and publishing

## 📦 Docker Images

The application is automatically built and published to GitHub Container Registry:

- **Frontend**: `ghcr.io/abderraza8k/emptymug-project-frontend:latest`
- **Backend**: `ghcr.io/abderraza8k/emptymug-project-backend:latest`

### Quick Deploy with Docker

```bash
# Using Docker Compose (Recommended)
docker-compose -f docker-compose.prod.yml up -d

# Or run individual containers
docker run -p 3000:80 ghcr.io/abderraza8k/emptymug-project-frontend:latest
docker run -p 8000:8000 ghcr.io/abderraza8k/emptymug-project-backend:latest
```

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Hook Form** for form handling
- **Axios** for API calls

### Backend
- **FastAPI** for REST API
- **Pydantic** for data validation
- **Aiosmtplib** for email sending
- **Python 3.11**

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker and Docker Compose
- VS Code (recommended for dev container support)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd emptymug-website
   ```

2. **Configure Environment Variables**
   ```bash
   cp backend/.env.example backend/.env
   ```
   
   Edit `backend/.env` and update the email configuration:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=contact@emptymug.fr
   EMAIL_PASSWORD=your_app_password_here
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Ollama: http://localhost:11434

### Using Dev Containers (Recommended)

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Select "Dev Containers: Reopen in Container"
5. VS Code will build and open the dev container automatically

## 🗄️ Database Configuration

The application supports multiple database backends:

### In-Memory Database (Default)
Perfect for development and testing:
```env
DATABASE_TYPE=memory
```

### PostgreSQL (Recommended for Production)
```env
DATABASE_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=emptymug
```

### DynamoDB (AWS Cloud)
```env
DATABASE_TYPE=dynamodb
DYNAMODB_REGION=us-east-1
DYNAMODB_TABLE_NAME=emptymug_contacts
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

## 🤖 AI Content Moderation

The application uses Ollama for AI-powered content moderation:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Setup Ollama
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Start service: `ollama serve`
3. Pull model: `ollama pull llama2`

## 📧 Email Configuration (Legacy)

The contact form sends emails using SMTP. For Gmail:

1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" for the application
3. Use the app password in the `EMAIL_PASSWORD` environment variable

For other email providers, update the `EMAIL_HOST` and `EMAIL_PORT` accordingly.

## 🎨 Design Features

- **Glass Effect**: Modern glassmorphism design elements
- **Gradient Backgrounds**: Beautiful gradient overlays
- **Floating Animations**: Subtle floating animations for visual appeal
- **Smooth Transitions**: All interactions have smooth transitions
- **Mobile First**: Responsive design that works on all screen sizes

## 📱 Contact Form Features

- **Form Validation**: Client-side and server-side validation
- **Country Code Selection**: Dropdown with country flags and dial codes
- **Email Formatting**: Professional HTML email templates
- **Error Handling**: Comprehensive error handling and user feedback
- **Success States**: Clear success/error feedback to users

## 🌍 Internationalization

The contact form includes a comprehensive list of countries with their:
- Country flags (emoji)
- Dial codes
- Country names
- Sorted alphabetically for easy selection

Note: Israel is excluded from the country list as requested.

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Building for Production
```bash
# Build frontend
cd frontend
npm run build

# The backend is ready for production deployment as-is
```

## 📝 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /api/contact` - Submit contact form

## 🚀 Deployment

The application is containerized and ready for deployment to any container orchestration platform:

- Docker images for both frontend and backend
- Environment variable configuration
- Health check endpoints
- CORS configuration for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright 2024 EmptyMug

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

Built with ❤️ for EmptyMug - Creating digital experiences that matter.
