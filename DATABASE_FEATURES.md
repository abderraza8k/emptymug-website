# Database Integration and Content Moderation Features

## Overview

The EmptyMug website backend has been enhanced with:
- **Database storage** for contact form submissions
- **Multi-database support** (In-memory, PostgreSQL, DynamoDB)
- **Advanced validation** for email, phone numbers, and user input
- **AI-powered content moderation** using Ollama LLM integration
- **Interactive Voronoi background** on the frontend

## Database Configuration

### Supported Databases

1. **In-Memory Database** (Development)
   - Perfect for development and testing
   - No external dependencies required
   - Data is lost when the application restarts

2. **PostgreSQL** (Recommended for Production)
   - Full-featured relational database
   - Automatic schema creation on startup
   - Includes DDL file for manual setup

3. **DynamoDB** (AWS Cloud)
   - Serverless NoSQL database
   - Auto-scaling capabilities
   - Pay-per-request pricing model

### Configuration

Set the database type in your `.env` file:

```env
# Use in-memory database
DATABASE_TYPE=memory

# Use PostgreSQL
DATABASE_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=emptymug

# Use DynamoDB
DATABASE_TYPE=dynamodb
DYNAMODB_REGION=us-east-1
DYNAMODB_TABLE_NAME=emptymug_contacts
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### PostgreSQL Setup

The application automatically creates the required schema on startup. For manual setup:

```bash
# Run the DDL script
psql -h localhost -U postgres -d emptymug -f backend/database/schema.sql
```

## Content Moderation with LLM

### Ollama Integration

The application uses Ollama for AI-powered content moderation:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### Features

- **Profanity detection** - Identifies and blocks inappropriate language
- **Hate speech detection** - Filters discriminatory content
- **Spam detection** - Identifies promotional or spam content
- **Tone analysis** - Ensures professional communication
- **Fallback system** - Uses rule-based filtering if LLM is unavailable

### Setup Ollama

1. Install Ollama:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. Start Ollama and pull the model:
   ```bash
   ollama serve
   ollama pull llama2
   ```

## Enhanced Validation

### Email Validation
- Uses `email-validator` library
- Validates format and deliverability
- Normalizes email addresses

### Phone Number Validation
- International format support
- Country code validation
- Uses `phonenumbers` library
- Formats numbers to international standard

### Name Validation
- Supports international characters
- Minimum/maximum length validation
- Prevents special characters except hyphens and apostrophes

### Message Validation
- Minimum 10 characters
- Maximum 5000 characters
- Content moderation using LLM

## Frontend Enhancements

### Interactive Voronoi Background

The homepage now features a subtle animated Voronoi diagram:

- **Responsive design** - Adapts to screen size
- **Smooth animations** - Gentle movement of Voronoi cells
- **Subtle colors** - Professional color palette
- **Performance optimized** - Uses HTML5 Canvas for smooth rendering

### Features
- Animated points that bounce off boundaries
- Voronoi cells that update in real-time
- Customizable opacity and colors
- Responsive to window resizing

## API Endpoints

### Submit Contact Form
```http
POST /api/contact
Content-Type: application/json

{
  "fullName": "John Doe",
  "email": "john@example.com",
  "phoneNumber": "+1234567890",
  "countryCode": "US",
  "message": "Hello, I'd like to get in touch!"
}
```

### Get Contacts (Admin)
```http
GET /api/contacts?limit=50&offset=0
```

### Get Specific Contact
```http
GET /api/contacts/{contact_id}
```

## Docker Development Setup

### Quick Start
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Services Included
- **Frontend** - React development server
- **Backend** - FastAPI with hot reload
- **PostgreSQL** - Database with automatic schema setup
- **Ollama** - LLM service for content moderation

### Environment Variables

The development setup includes:
- PostgreSQL database automatically configured
- Ollama service with llama2 model
- CORS enabled for frontend development
- Hot reload for both frontend and backend

## Security Features

### Input Validation
- All inputs are validated before processing
- SQL injection prevention through ORM
- XSS prevention through input sanitization

### Content Moderation
- AI-powered content filtering
- Fallback rule-based system
- Configurable moderation policies

### Database Security
- Non-root user in Docker containers
- Connection pooling for PostgreSQL
- Encrypted connections support

## Performance Optimizations

### Database
- Connection pooling
- Indexed queries
- Prepared statements

### Frontend
- Canvas-based Voronoi rendering
- Optimized animation loops
- Responsive design patterns

### Backend
- Async/await throughout
- Efficient validation pipeline
- Caching for validation results

## Monitoring and Logging

### Health Checks
- Database connection status
- LLM service availability
- Comprehensive error logging

### Metrics
- Contact submission rates
- Content moderation statistics
- Database performance metrics

## Deployment Notes

### Production Checklist
1. Set `DATABASE_TYPE=postgres` or `DATABASE_TYPE=dynamodb`
2. Configure proper database credentials
3. Set up Ollama service or use cloud LLM API
4. Enable HTTPS for secure communication
5. Set up proper CORS origins
6. Configure monitoring and logging

### Environment Variables
Copy `.env.example` to `.env` and configure all required variables for your environment.

### Scaling Considerations
- Use read replicas for PostgreSQL
- Configure DynamoDB auto-scaling
- Set up load balancing for Ollama
- Use Redis for session management if needed

This enhanced setup provides a robust, scalable foundation for the EmptyMug website with professional-grade features for content management and user interaction.
