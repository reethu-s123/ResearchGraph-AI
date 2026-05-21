"""
ResearchGraph AI - Advanced Configuration
Production-ready setup guide
"""

# PRODUCTION DEPLOYMENT GUIDE

## Environment Setup

### 1. Server Requirements
- Python 3.8+
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Fast internet connection

### 2. Production Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn  # For production serving
```

### 3. Environment Configuration
```bash
# Copy and edit environment file
cp .env.example .env

# Set production variables
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=WARNING
```

## Running in Production

### Option 1: Streamlit Cloud
```bash
# Push to GitHub
git push origin main

# Deploy on Streamlit Cloud
# Visit: https://streamlit.io/cloud
```

### Option 2: Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Deploy Docker:
```bash
docker build -t researchgraph-ai .
docker run -p 8501:8501 researchgraph-ai
```

### Option 3: Linux Server
```bash
# Install supervisor for process management
sudo apt-get install supervisor

# Create config file: /etc/supervisor/conf.d/researchgraph.conf
[program:researchgraph]
directory=/home/user/ResearchGraph-AI
command=/home/user/ResearchGraph-AI/venv/bin/streamlit run app.py
autostart=true
autorestart=true
```

## Performance Optimization

### 1. Caching Strategy
- Enable Redis for distributed caching
- Increase CACHE_TTL for slower changing data
- Clear cache periodically

### 2. Database Optimization
- Use Neo4j for large graphs
- Index frequently queried fields
- Archive old data regularly

### 3. API Rate Limiting
- Implement request throttling
- Use connection pooling
- Cache API responses

## Monitoring & Logging

### 1. Application Monitoring
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5)
logging.getLogger().addHandler(handler)
```

### 2. Performance Metrics
- Monitor API response times
- Track model inference latency
- Log error rates

### 3. Health Checks
```bash
# Health check endpoint
curl http://localhost:8501/health
```

## Security Best Practices

1. **API Keys**
   - Store in environment variables
   - Rotate regularly
   - Use separate keys for dev/prod

2. **Data Protection**
   - Enable HTTPS
   - Use secure cookies
   - Validate all inputs

3. **Authentication**
   - Implement user authentication
   - Use OAuth for third-party integrations
   - Rate limit auth attempts

## Scaling

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer
- Shared cache layer (Redis)

### Vertical Scaling
- Increase server resources
- Use GPU for model inference
- Optimize database queries

## Backup & Recovery

```bash
# Backup data
tar -czf researchgraph-backup.tar.gz data/ .cache/

# Restore
tar -xzf researchgraph-backup.tar.gz
```

## Troubleshooting

### High Memory Usage
```bash
# Monitor memory
free -h

# Reduce batch size
MAX_PAPERS_PER_SEARCH=10
```

### Slow Response Times
```bash
# Check API latency
time curl https://www.ebi.ac.uk/europepmc/webservices/rest/search

# Enable caching
CACHE_ENABLED=true
CACHE_TTL=7200
```

### API Failures
- Check Europe PMC status
- Verify network connectivity
- Check API key validity
