# Persona API - Operations & Monitoring Guide

Complete guide for monitoring, maintaining, and troubleshooting Persona API in production.

## Table of Contents

- [Monitoring](#monitoring)
- [Logging](#logging)
- [Health Checks](#health-checks)
- [Performance Optimization](#performance-optimization)
- [Security](#security)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

---

## Monitoring

### Health Check Endpoint

```bash
curl http://api.example.com/health
```

Expected response (2xx status):
```json
{
  "status": "healthy",
  "service": "persona-api",
  "environment": "production"
}
```

### Key Metrics

**Track these metrics:**

1. **Endpoint Performance**
   - Response time per endpoint
   - Request count per endpoint
   - Error rate per endpoint

2. **System Resources**
   - CPU usage
   - Memory usage
   - Disk usage
   - Network I/O

3. **Business Metrics**
   - Personas created per day
   - API calls per day
   - Average response time
   - Error count per hour

### Monitoring Tools

#### CloudWatch (AWS)

```bash
# View logs
aws logs tail /ecs/persona-api --follow

# Create metric alarm
aws cloudwatch put-metric-alarm \
  --alarm-name persona-api-high-cpu \
  --alarm-description "Alert if CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

#### Prometheus + Grafana

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'persona-api'
    static_configs:
      - targets: ['localhost:8080']
```

#### Datadog

```yaml
# datadog-agent config
logs:
  - type: file
    path: /var/log/persona-api/app.log
    service: persona-api
    source: python
```

---

## Logging

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for unusual events
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate action

### Log Location

```bash
# Docker container
docker logs persona-api

# Log file
tail -f logs/app.log

# Docker Compose
docker-compose logs -f persona-api
```

### Log Analysis

#### View errors

```bash
grep ERROR logs/app.log | tail -20
```

#### View specific service logs

```bash
grep "PersonaService\|PersonaSynthesizer\|PersonaLLMChain" logs/app.log
```

#### View slow requests

```bash
grep "response time\|latency" logs/app.log | grep -v "< 1000ms"
```

---

## Health Checks

### Application Health

```bash
# Health check
curl http://localhost:8080/health

# Root endpoint
curl http://localhost:8080/

# API documentation (Swagger)
curl http://localhost:8080/docs
```

### Database Health

```python
# Test connection
from app.db.supabase_client import get_supabase_client

client = get_supabase_client()
is_healthy = client.is_connected()
print(f"Database healthy: {is_healthy}")
```

### Dependency Health

- OpenAI API: Check status at https://status.openai.com
- Supabase: Check status at https://status.supabase.com
- Network: `ping supabase-project.supabase.co`

---

## Performance Optimization

### API Response Times

**Current targets:**
- GET /v1/persona: < 100ms
- GET /v1/persona/{id}: < 100ms
- POST /v1/persona: 5-10s (includes LLM generation)
- GET /v1/persona/search: < 500ms
- GET /v1/persona/stats: < 1s

### Optimization Strategies

#### 1. Database Queries

```sql
-- Enable query analysis
EXPLAIN ANALYZE
SELECT * FROM personas WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC LIMIT 100;

-- Add indexes for common queries
CREATE INDEX idx_personas_created_at_desc ON personas(created_at DESC);
```

#### 2. Caching (Future)

```python
# Cache strategies to implement
- Cache persona search results (5 min TTL)
- Cache stats calculations (1 hour TTL)
- Cache export data (10 min TTL)
```

#### 3. Batch Operations

```python
# Optimize batch processing
- Process in parallel batches (max 10 concurrent)
- Use asyncio.gather() for concurrent requests
- Implement rate limiting for LLM API
```

### Performance Monitoring

```bash
# Monitor response times
curl -w "\nTime: %{time_total}s\n" http://localhost:8080/v1/persona?limit=10

# Load testing (using Apache Bench)
ab -n 100 -c 10 http://localhost:8080/health

# Load testing (using wrk)
wrk -t4 -c100 -d30s http://localhost:8080/health
```

---

## Security

### API Security

**Implemented:**
- Input validation (Pydantic models)
- Rate limiting (implement if needed)
- CORS configuration
- Error message sanitization
- No secrets in logs

**To Implement:**
- API key authentication
- JWT token validation
- Request signing
- SQL injection prevention (ORM handles)
- XSS prevention (API, not web UI)

### Environment Security

```bash
# Use secrets manager (not .env in production)
# AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id persona-api/openai-key

# Supabase Secrets
supabase secrets list
supabase secrets set OPENAI_API_KEY=sk-...

# Kubernetes Secrets
kubectl create secret generic persona-api-secrets \
  --from-literal=OPENAI_API_KEY=sk-...
```

### Network Security

```bash
# Use HTTPS in production
https://api.example.com/v1/persona

# Restrict CORS
CORSMiddleware(
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

# Security headers
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.example.com"])
```

---

## Backup & Recovery

### Database Backup

#### Supabase Backups

```bash
# Automatic daily backups (Supabase)
# Manual backup via dashboard
# Export SQL via Supabase dashboard

# Restore from backup
1. Download backup SQL
2. Connect to database
3. Run: psql -d persona_db -f backup.sql
```

#### Local PostgreSQL Backups

```bash
# Full backup
pg_dump -U postgres persona_db > backup.sql

# Restore
psql -U postgres persona_db < backup.sql

# Compressed backup
pg_dump -U postgres -Fc persona_db > backup.dump
pg_restore -U postgres -d persona_db backup.dump
```

### Application Recovery

**Disaster Recovery Plan:**

1. **Data Loss**
   - Restore from most recent backup
   - Verify data integrity
   - Restart application

2. **Service Unavailable**
   - Check logs for errors
   - Restart container/service
   - Verify dependencies (OpenAI, Supabase)
   - Failover to standby instance

3. **Performance Degradation**
   - Check database connection
   - Monitor CPU/memory
   - Review slow queries
   - Scale horizontally/vertically

---

## Troubleshooting

### Common Issues

#### 1. Application Won't Start

**Symptoms**: Container exits with error code

**Debug Steps:**
```bash
# Check logs
docker logs persona-api

# Common causes:
# - Missing environment variables
# - Invalid database connection
# - Port already in use
```

**Solutions:**
```bash
# Verify environment
docker inspect persona-api | grep Env

# Change port if needed
docker run -p 8081:8080 persona-api:latest

# Remove conflicting containers
docker ps -a | grep persona-api
docker rm <container-id>
```

#### 2. High Memory Usage

**Symptoms**: Container reaches memory limit

**Debug Steps:**
```bash
# Monitor memory
docker stats persona-api

# Check logs for memory errors
grep -i "memory\|oom" logs/app.log
```

**Solutions:**
```bash
# Increase memory limit
docker run -m 1g persona-api:latest

# Reduce batch size (in code)
# Implement pagination for large queries
# Enable garbage collection optimization
```

#### 3. Database Connection Errors

**Symptoms**: "Failed to connect to Supabase"

**Debug Steps:**
```bash
# Test connection directly
python -c "
from app.db.supabase_client import get_supabase_client
client = get_supabase_client()
print(f'Connected: {client.is_connected()}')
"

# Check network
ping <supabase-url>
curl https://<supabase-url>/health
```

**Solutions:**
```bash
# Verify credentials
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY

# Check Supabase status
# https://status.supabase.com

# Restart application
docker restart persona-api
```

#### 4. Slow API Responses

**Symptoms**: POST /v1/persona taking >30 seconds

**Debug Steps:**
```bash
# Check OpenAI API
# Visit: https://status.openai.com

# Monitor request
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/v1/persona

# Profile code
# Add timing logs around LLM calls
```

**Solutions:**
```bash
# Check OpenAI quota
# Review API rate limits

# Optimize prompts
# Reduce token count in generation

# Implement timeout
# Set timeout: 30 seconds max per request
```

#### 5. High Error Rate

**Symptoms**: 5xx errors in logs

**Debug Steps:**
```bash
# Count errors
grep -c "ERROR\|500\|exception" logs/app.log

# See error types
grep "ERROR" logs/app.log | cut -d' ' -f3- | sort | uniq -c
```

**Solutions:**
```bash
# Review recent changes
git log --oneline -10

# Check dependencies
# - OpenAI API status
# - Database connectivity
# - Network issues

# Rollback if needed
# docker run persona-api:previous-tag
```

### Support Commands

```bash
# Get container ID
docker ps | grep persona-api

# View full logs
docker logs <container-id> --tail=100

# Access container shell
docker exec -it <container-id> /bin/bash

# Monitor in real-time
docker stats <container-id>

# Stop and remove
docker stop <container-id>
docker rm <container-id>
```

---

## Escalation Procedures

**Critical Issue** (Service down):
1. Page on-call engineer
2. Check Supabase status
3. Check OpenAI status
4. Restart application
5. Check database connectivity
6. Review recent deployments

**High Priority** (Performance degraded):
1. Notify team
2. Monitor metrics
3. Check resource usage
4. Review logs
5. Scale resources if needed

**Medium Priority** (Intermittent errors):
1. Investigate root cause
2. Monitor frequency
3. Patch or schedule fix
4. Test thoroughly

---

**Last Updated**: 2025-11-07
