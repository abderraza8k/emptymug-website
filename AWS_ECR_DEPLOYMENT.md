# AWS ECR Deployment Setup

This document explains how to set up the GitHub Action workflow for building and deploying Docker images to AWS ECR.

## Prerequisites

1. **AWS Account** with ECR access
2. **GitHub Repository** with appropriate permissions
3. **AWS IAM User** with ECR permissions

## AWS Setup

### 1. Create IAM User

Create an IAM user with programmatic access and attach the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:CreateRepository",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage",
                "ecr:BatchDeleteImage",
                "ecr:StartImageScan",
                "ecr:DescribeImageScanFindings",
                "ecr:PutLifecyclePolicy"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. Get AWS Credentials

After creating the IAM user, save the:
- Access Key ID
- Secret Access Key

## GitHub Secrets Setup

Go to your GitHub repository settings and add the following secrets:

### Repository Secrets

Navigate to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key | IAM user secret key |

## Workflow Configuration

The workflow is configured in `.github/workflows/deploy-to-ecr.yml` with the following settings:

### Environment Variables

```yaml
env:
  AWS_REGION: us-east-1  # Change this to your preferred region
  ECR_REPOSITORY_FRONTEND: emptymug-frontend
  ECR_REPOSITORY_BACKEND: emptymug-backend
```

### Customization

You can customize the workflow by modifying:

1. **AWS Region**: Change `AWS_REGION` in the workflow file
2. **Repository Names**: Modify `ECR_REPOSITORY_FRONTEND` and `ECR_REPOSITORY_BACKEND`
3. **Trigger Conditions**: Adjust the `on:` section for different trigger conditions

## Workflow Features

### 🚀 **Build and Push**
- Multi-architecture builds (AMD64 + ARM64)
- Automatic ECR repository creation
- Image caching for faster builds
- Tags images with both commit SHA and `latest`

### 🔒 **Security**
- Automatic vulnerability scanning on push
- Lifecycle policies to manage image retention
- Secure credential handling via GitHub secrets

### 📊 **Monitoring**
- Build summaries in GitHub Actions
- Security scan results in workflow summary
- Detailed logging for troubleshooting

## Usage

### Automatic Deployment

The workflow triggers automatically on:
- Push to `main` branch (with changes in `apps/emptymug-website/`)
- Pull requests to `main` branch
- Manual dispatch via GitHub Actions UI

### Manual Deployment

1. Go to your repository's Actions tab
2. Select "Build and Deploy to AWS ECR"
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## ECR Repository Structure

After the first run, you'll have:

```
AWS ECR Repositories:
├── emptymug-frontend
│   ├── latest
│   └── <commit-sha>
└── emptymug-backend
    ├── latest
    └── <commit-sha>
```

## Image URIs

After deployment, your images will be available at:

```bash
# Frontend
<account-id>.dkr.ecr.<region>.amazonaws.com/emptymug-frontend:latest
<account-id>.dkr.ecr.<region>.amazonaws.com/emptymug-frontend:<commit-sha>

# Backend
<account-id>.dkr.ecr.<region>.amazonaws.com/emptymug-backend:latest
<account-id>.dkr.ecr.<region>.amazonaws.com/emptymug-backend:<commit-sha>
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure IAM user has all required ECR permissions
2. **Repository Not Found**: The workflow will automatically create repositories
3. **Build Failures**: Check the Dockerfile paths and build context
4. **Scanning Issues**: Scans may take time to complete; results appear in subsequent runs

### Debugging

- Check the Actions tab for detailed logs
- Verify AWS credentials are correctly set in secrets
- Ensure Docker files exist in the specified paths

## Cost Optimization

- Lifecycle policies automatically clean up old images (keeps last 10)
- Multi-arch builds may increase storage costs but improve compatibility
- Consider using AWS ECR lifecycle policies for additional cost control

## Security Considerations

- Never commit AWS credentials to the repository
- Use least-privilege IAM policies
- Regularly rotate AWS access keys
- Monitor ECR access logs
- Enable AWS CloudTrail for audit logging
