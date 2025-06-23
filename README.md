# EmptyMug Website

A modern, responsive website for EmptyMug built with React and Python FastAPI, featuring a sleek Apple-inspired design with smooth animations.

## 🚀 Features

- **Modern Design**: Apple-inspired UI with clean aesthetics
- **Responsive**: Works perfectly on all devices
- **Smooth Animations**: Subtle animations powered by Framer Motion
- **Contact Form**: Advanced contact form with country code selection
- **Email Integration**: Automatic email sending to contact@emptymug.fr
- **TypeScript**: Full TypeScript support for better development experience
- **Dev Containers**: Ready-to-use development environment

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

### Using Dev Containers (Recommended)

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Select "Dev Containers: Reopen in Container"
5. VS Code will build and open the dev container automatically

## 📧 Email Configuration

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

This project is proprietary to EmptyMug.

---

Built with ❤️ for EmptyMug - Creating digital experiences that matter.
