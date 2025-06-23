# EmptyMug Website - Deployment Guide

## 🚀 GitHub Container Registry

This project automatically builds and publishes Docker images to GitHub Container Registry (GHCR) when code is pushed to the main branch or when tags are created.

### 📦 Published Images

- **Frontend**: `ghcr.io/your-username/emptymug-project-frontend:latest`
- **Backend**: `ghcr.io/your-username/emptymug-project-backend:latest`

### 🔧 Automatic Builds

The GitHub Actions workflow automatically:

1. **On Push to Main/Develop**: Builds and publishes images with branch name and `latest` tags
2. **On Pull Requests**: Builds images for testing (no push to registry)
3. **On Tags** (e.g., `v1.0.0`): Creates releases with version-specific tags

### 🏃‍♂️ Quick Deployment

#### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/emptymug-project.git
cd emptymug-project/apps/emptymug-website

# Create environment file
cp backend/.env.example .env
# Edit .env with your email configuration

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

#### Option 2: Individual Containers

```bash
# Run Backend
docker run -d \
  --name emptymug-backend \
  -p 8000:8000 \
  -e EMAIL_HOST=smtp.gmail.com \
  -e EMAIL_PORT=587 \
  -e EMAIL_USER=contact@emptymug.fr \
  -e EMAIL_PASSWORD=your_app_password \
  -e CORS_ORIGINS=http://localhost:3000 \
  ghcr.io/your-username/emptymug-project-backend:latest

# Run Frontend
docker run -d \
  --name emptymug-frontend \
  -p 3000:80 \
  ghcr.io/your-username/emptymug-project-frontend:latest
```

### 🔐 Authentication

To pull images from GHCR, you may need to authenticate:

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u username --password-stdin

# Or using GitHub CLI
gh auth token | docker login ghcr.io -u username --password-stdin
```

### 🏷️ Image Tags

Images are tagged with:

- `latest` - Latest build from main branch
- `main` - Latest build from main branch
- `develop` - Latest build from develop branch
- `v1.0.0` - Specific version releases
- `sha-<commit>` - Specific commit builds

### 📊 Monitoring

Health checks are included:

- **Backend**: `http://localhost:8000/health`
- **Frontend**: Nginx serves static files with proper headers

### 🔧 Environment Variables

**Backend**:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=contact@emptymug.fr
EMAIL_PASSWORD=your_app_password_here
CORS_ORIGINS=http://localhost:3000,https://emptymug.fr
```

### 🌍 Production Deployment

For production deployment:

1. **Update docker-compose.prod.yml** with your actual image registry path
2. **Set up proper DNS** pointing to your server
3. **Configure SSL/TLS** using a reverse proxy like Nginx or Traefik
4. **Set production environment variables**
5. **Set up monitoring and logging**

### 📝 Creating Releases

To create a new release:

```bash
# Tag a new version
git tag v1.0.0
git push origin v1.0.0
```

This will automatically:
- Build both Docker images
- Push them with version tags
- Create a GitHub release with release notes
- Make images available at `ghcr.io/your-username/emptymug-project-{frontend,backend}:v1.0.0`

### 🔍 Troubleshooting

**Image pull issues**:
- Ensure you're authenticated with GHCR
- Check if the repository has public package visibility
- Verify the correct image name and tag

**Build failures**:
- Check GitHub Actions logs
- Ensure all required files are committed
- Verify Dockerfile syntax

**Runtime issues**:
- Check container logs: `docker logs emptymug-backend`
- Verify environment variables are set correctly
- Ensure all required ports are exposed
