# Deployment Guide - Forensic Cyber Tech Cloud Messenger

This guide provides step-by-step instructions for deploying the Forensic Cyber Tech Cloud Messenger to various environments.

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- Domain name (for production)
- SSL certificates (for production)
- Minimum 8GB RAM, 20GB disk space

## Local Development Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/forensic-messenger.git
cd forensic-messenger
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and update the following critical values:

```env
SECRET_KEY=your-unique-secret-key-min-32-chars
ENCRYPTION_KEY=your-encryption-key-exactly-32-chars
POSTGRES_PASSWORD=strong-postgres-password
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Verify Deployment

```bash
# Check all services are healthy
docker-compose ps

# View logs
docker-compose logs -f backend
```

### 5. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- MinIO Console: http://localhost:9001 (admin/minioadmin)
- Prometheus: http://localhost:9090

## Production Deployment

### Option 1: Docker Compose (Single Server)

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Clone and Configure

```bash
git clone https://github.com/YOUR_USERNAME/forensic-messenger.git
cd forensic-messenger

# Create production environment file
cp .env.example .env
nano .env
```

**Critical Production Settings:**

```env
DEBUG=False
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ENCRYPTION_KEY=<generate-with-openssl-rand-hex-32>

# Use strong passwords
POSTGRES_PASSWORD=<strong-password>
REDIS_PASSWORD=<strong-password>

# Production URLs
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### 3. SSL/TLS Setup

Create `nginx-ssl.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

#### 4. Deploy

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify health
curl http://localhost:8000/health
```

### Option 2: Kubernetes Deployment

#### 1. Create Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: forensic-messenger
```

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: forensic-messenger
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/forensic-messenger-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: POSTGRES_SERVER
          value: postgres-service
        - name: REDIS_HOST
          value: redis-service
        envFrom:
        - secretRef:
            name: backend-secrets
```

#### 2. Deploy to Kubernetes

```bash
kubectl apply -f k8s/
kubectl get pods -n forensic-messenger
```

### Option 3: Cloud Platform Deployment

#### AWS ECS/Fargate

1. Push images to ECR
2. Create ECS task definitions
3. Set up Application Load Balancer
4. Configure RDS for PostgreSQL
5. Use ElastiCache for Redis
6. Use DocumentDB for MongoDB
7. Use OpenSearch for Elasticsearch

#### Google Cloud Run

```bash
# Build and push images
gcloud builds submit --tag gcr.io/PROJECT_ID/backend
gcloud builds submit --tag gcr.io/PROJECT_ID/frontend

# Deploy services
gcloud run deploy backend --image gcr.io/PROJECT_ID/backend --platform managed
gcloud run deploy frontend --image gcr.io/PROJECT_ID/frontend --platform managed
```

## Database Migrations

### Initial Setup

```bash
# Enter backend container
docker-compose exec backend bash

# Run migrations (when implemented)
alembic upgrade head
```

## Backup Strategy

### Automated Backups

```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U forensic_user forensic_messenger > backup_$(date +%Y%m%d).sql

# MongoDB backup
docker-compose exec mongodb mongodump --out=/backup/$(date +%Y%m%d)

# Redis backup
docker-compose exec redis redis-cli SAVE
```

### Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker-compose exec -T postgres pg_dump -U forensic_user forensic_messenger > $BACKUP_DIR/postgres.sql

# Backup MongoDB
docker-compose exec -T mongodb mongodump --archive > $BACKUP_DIR/mongodb.archive

# Backup Redis
docker-compose exec -T redis redis-cli --rdb $BACKUP_DIR/dump.rdb

# Compress
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

## Monitoring

### Prometheus + Grafana

```yaml
# Add to docker-compose.yml
grafana:
  image: grafana/grafana:latest
  ports:
    - "3001:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
  volumes:
    - grafana_data:/var/lib/grafana
```

Access Grafana at http://localhost:3001

### Log Aggregation

Use ELK Stack or cloud logging:

```yaml
# docker-compose.yml
elasticsearch-logging:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
  
logstash:
  image: docker.elastic.co/logstash/logstash:8.11.0
  
kibana:
  image: docker.elastic.co/kibana/kibana:8.11.0
  ports:
    - "5601:5601"
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend instances
docker-compose up -d --scale backend=3

# Kubernetes scaling
kubectl scale deployment backend --replicas=5 -n forensic-messenger
```

### Load Balancing

Use Nginx or cloud load balancers:

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Generate unique SECRET_KEY and ENCRYPTION_KEY
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up VPN for database access
- [ ] Enable database encryption at rest
- [ ] Configure OAuth2 providers
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Implement backup strategy
- [ ] Configure monitoring alerts

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs backend

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build backend
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose exec postgres psql -U forensic_user -d forensic_messenger

# Check MongoDB
docker-compose exec mongodb mongosh
```

### WebSocket Connection Fails

- Verify Redis is running
- Check CORS configuration
- Ensure WebSocket proxy is configured in Nginx

## Performance Optimization

1. **Database Indexing**: Ensure proper indexes on frequently queried fields
2. **Redis Caching**: Cache frequently accessed data
3. **CDN**: Use CDN for static assets
4. **Connection Pooling**: Configure appropriate pool sizes
5. **Compression**: Enable gzip compression in Nginx

## Support

For issues and questions:
- GitHub Issues: https://github.com/YOUR_USERNAME/forensic-messenger/issues
- Documentation: See README.md and WEBSOCKET.md
- Email: support@forensiccybertech.com

---

**Deployment completed successfully!** 🚀
