# Persona API - Deployment Guide

Complete guide for deploying Persona API to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- Docker & Docker Compose (for containerized deployment)
- Python 3.11+ (for local development)
- OpenAI API Key ([get one here](https://platform.openai.com/api-keys))
- Supabase account & project ([create one here](https://supabase.com))

### Optional

- PostgreSQL 15+ (for local development without Docker)
- Git for version control

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/cr-nattress/persona-api.git
cd persona-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov  # For testing
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxx...
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### 5. Run Locally

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Visit http://localhost:8080 for API, http://localhost:8080/docs for Swagger UI.

---

## Docker Deployment

### Local Docker Setup

#### 1. Build Image

```bash
docker build -t persona-api:latest .
```

#### 2. Run Container

```bash
docker run -it \
  -p 8080:8080 \
  -e OPENAI_API_KEY=sk-... \
  -e SUPABASE_URL=https://xxxxx.supabase.co \
  -e SUPABASE_ANON_KEY=eyJxx... \
  persona-api:latest
```

#### 3. Using Docker Compose

```bash
# Create .env file with required variables
cp .env.example .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f persona-api

# Stop services
docker-compose down
```

### Health Check

```bash
curl http://localhost:8080/health
# Response: {"status": "healthy", "service": "persona-api"}
```

### View Logs

```bash
docker logs persona-api -f
# Or with Docker Compose
docker-compose logs -f persona-api
```

---

## Production Deployment

### AWS Deployment

#### Option 1: ECS (Fargate)

1. **Create ECR Repository**

```bash
aws ecr create-repository --repository-name persona-api
```

2. **Build and Push Image**

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t persona-api:latest .

docker tag persona-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/persona-api:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/persona-api:latest
```

3. **Create ECS Task Definition**

```json
{
  "family": "persona-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "persona-api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/persona-api:latest",
      "portMappings": [{"containerPort": 8080}],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"},
        {"name": "LOG_LEVEL", "value": "INFO"}
      ],
      "secrets": [
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "SUPABASE_URL", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "SUPABASE_ANON_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ]
}
```

4. **Create ECS Service**

```bash
aws ecs create-service \
  --cluster persona-api-cluster \
  --service-name persona-api \
  --task-definition persona-api \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

#### Option 2: Kubernetes (EKS)

1. **Create Docker Image** (as above)

2. **Push to ECR** (as above)

3. **Create Kubernetes Deployment**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: persona-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: persona-api
  template:
    metadata:
      labels:
        app: persona-api
    spec:
      containers:
      - name: persona-api
        image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/persona-api:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        envFrom:
        - secretRef:
            name: persona-api-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: persona-api-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: persona-api
```

4. **Deploy to EKS**

```bash
kubectl apply -f deployment.yaml
```

### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/[PROJECT_ID]/persona-api

# Deploy to Cloud Run
gcloud run deploy persona-api \
  --image gcr.io/[PROJECT_ID]/persona-api \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars ENVIRONMENT=production,LOG_LEVEL=INFO \
  --set-secrets OPENAI_API_KEY=openai-key:latest,SUPABASE_URL=supabase-url:latest,SUPABASE_ANON_KEY=supabase-key:latest
```

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create persona-api

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set SUPABASE_URL=https://...
heroku config:set SUPABASE_ANON_KEY=eyJ...

# Deploy
git push heroku main
```

---

## Environment Configuration

### Development

```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
OPENAI_MODEL=gpt-4o-mini
DEBUG=True
```

### Production

```env
ENVIRONMENT=production
LOG_LEVEL=INFO
OPENAI_MODEL=gpt-4o-mini
DEBUG=False
```

---

## Database Setup

### Supabase (Recommended)

1. Create Supabase project
2. Get connection credentials from Project Settings
3. Run migrations in SQL editor:

```sql
-- Create personas table
CREATE TABLE public.personas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  raw_text TEXT NOT NULL,
  persona JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_personas_created_at ON public.personas(created_at);
CREATE INDEX idx_personas_updated_at ON public.personas(updated_at);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_timestamp
BEFORE UPDATE ON public.personas
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

### Local PostgreSQL

```bash
# Create database
createdb persona_db

# Run migrations
psql -d persona_db -f db/migrations/001_create_personas_table.sql
```

---

## Monitoring & Logging

### Application Logs

Logs are written to:
- Console (stdout)
- File: `logs/app.log` (with daily rotation)

### Health Check

```bash
curl http://api.example.com/health
```

Response:
```json
{
  "status": "healthy",
  "service": "persona-api",
  "environment": "production"
}
```

### Metrics Endpoint (Future)

- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

---

## Troubleshooting

### Application Won't Start

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/app:$PYTHONPATH

# Or run from project root
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Supabase Connection Fails

**Error**: `Failed to connect to Supabase`

**Solution**:
1. Verify credentials in `.env`
2. Check network connectivity
3. Ensure Supabase project is active
4. Check API key permissions

### Out of Memory

**Error**: Container killed with OOMKilled

**Solution**:
- Increase container memory limit
- Reduce batch processing size
- Enable pagination for large queries

### High Latency

**Error**: API requests taking >5 seconds

**Solution**:
1. Check OpenAI API status
2. Review database query performance
3. Check network latency
4. Enable response caching (future)

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Health check passing
- [ ] CORS settings appropriate for domain
- [ ] Logging configured and tested
- [ ] Error handling verified
- [ ] Performance benchmarks met
- [ ] Security settings reviewed
- [ ] Backup strategy in place
- [ ] Monitoring configured

---

## Support

For issues or questions:

1. Check logs: `docker-compose logs persona-api`
2. Review error messages and stack traces
3. Check application health: `curl http://localhost:8080/health`
4. Review documentation: This guide and API docs at `/docs`
5. Create GitHub issue: https://github.com/cr-nattress/persona-api/issues

---

**Last Updated**: 2025-11-07
