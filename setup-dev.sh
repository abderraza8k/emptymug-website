#!/bin/bash

# EmptyMug Website Development Setup Script

echo "🚀 Setting up EmptyMug Website Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📋 Creating environment file..."
    cp backend/.env.example backend/.env
    echo "✅ Environment file created. Please edit backend/.env with your email configuration."
else
    echo "✅ Environment file already exists."
fi

# Build and start the development environment
echo "🏗️  Building and starting development containers..."
docker-compose -f docker-compose.dev.yml up --build -d

echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "📝 Don't forget to configure your email settings in backend/.env"
echo ""
echo "To stop the development environment, run:"
echo "docker-compose -f docker-compose.dev.yml down"
