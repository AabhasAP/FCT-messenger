# Forensic Cyber Tech Cloud Messenger

A production-ready, enterprise-grade Slack alternative with real-time messaging, workspace management, and comprehensive security features.

## Features

### Core Functionality
- **Real-time Messaging** - WebSocket-based instant messaging with typing indicators
- **Workspaces & Channels** - Multi-tenant workspace isolation with public/private channels
- **Direct Messages** - One-on-one private conversations
- **Threads & Reactions** - Organized discussions with emoji reactions
- **File Sharing** - Upload and share files with preview support
- **Full-Text Search** - Elasticsearch-powered message search
- **Presence Tracking** - Real-time user online/away/offline status

### Security
- **JWT Authentication** - Secure token-based authentication with refresh tokens
- **Message Encryption** - AES-256 encryption for messages at rest
- **Rate Limiting** - Redis-based rate limiting to prevent abuse
- **RBAC** - Role-based access control at workspace level
- **Audit Logging** - Comprehensive audit trails for compliance

### Integrations
- **Bots** - Create custom bots with scoped permissions
- **Webhooks** - Integrate with external services (GitHub, CI/CD, etc.)
- **OAuth2** - Support for Google and GitHub login (configurable)

### Infrastructure
- **Microservice-Ready** - FastAPI backend designed for horizontal scaling
- **Multi-Database** - PostgreSQL, MongoDB, Redis, Elasticsearch
- **S3-Compatible Storage** - MinIO for file storage
- **Prometheus Metrics** - Built-in monitoring and observability
- **Docker** - Fully containerized with docker-compose

## Technology Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **PostgreSQL** - Relational data (users, workspaces, channels)
- **MongoDB** - Document storage (messages, threads)
- **Redis** - Caching, pub/sub, rate limiting
- **Elasticsearch** - Full-text search
- **MinIO** - S3-compatible object storage

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool
- **Axios** - HTTP client with interceptors
- **WebSocket** - Real-time communication

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Local development orchestration
- **Prometheus** - Metrics collection
- **Nginx** - Frontend serving and reverse proxy

## Quick Start

### Prerequisites
- Docker and Docker Compose
- 8GB RAM minimum
- Ports 3000, 8000, 5432, 27017, 6379, 9200, 9000 available

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd forensic-messenger
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to be healthy** (30-60 seconds)
   ```bash
   docker-compose ps
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001
   - Prometheus: http://localhost:9090

### First Steps

1. **Register a new account** at http://localhost:3000
2. **Create a workspace** after logging in
3. **Create channels** within your workspace
4. **Invite team members** via email
5. **Start messaging!**

## Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend    │────▶│  PostgreSQL │
│  (React)    │     │  (FastAPI)   │     │   (Users)   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ├────────────▶┌─────────────┐
                           │             │   MongoDB   │
                           │             │  (Messages) │
                           │             └─────────────┘
                           │
                           ├────────────▶┌─────────────┐
                           │             │    Redis    │
                           │             │ (Cache/Pub) │
                           │             └─────────────┘
                           │
                           ├────────────▶┌─────────────┐
                           │             │Elasticsearch│
                           │             │  (Search)   │
                           │             └─────────────┘
                           │
                           └────────────▶┌─────────────┐
                                         │    MinIO    │
                                         │   (Files)   │
                                         └─────────────┘
```

## Security Considerations

### Production Deployment
- Change all default passwords and secrets
- Enable TLS/SSL for all connections
- Configure OAuth2 providers
- Set up proper firewall rules
- Enable database backups
- Configure log aggregation
- Set up monitoring and alerting

### Environment Variables
Critical variables to change in production:
- `SECRET_KEY` - JWT signing key
- `ENCRYPTION_KEY` - Message encryption key
- Database passwords
- S3/MinIO credentials
- OAuth2 client secrets

## Monitoring

### Prometheus Metrics
Access Prometheus at http://localhost:9090

Available metrics:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `websocket_connections` - Active WebSocket connections
- `message_send_total` - Total messages sent

### Health Checks
- Backend: http://localhost:8000/health
- All services have Docker health checks configured

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build
```

### Database connection errors
```bash
# Check database health
docker-compose ps

# Reset databases (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

### WebSocket connection fails
- Ensure Redis is running
- Check CORS configuration
- Verify WebSocket proxy settings in Nginx

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Documentation: See `/docs` folder

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

---

**Built with ❤️ for secure enterprise communication**
