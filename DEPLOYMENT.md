# Pyralys Deployment Guide

Complete guide for deploying Pyralys to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Database Migrations](#database-migrations)
4. [Environment Configuration](#environment-configuration)
5. [Docker Production Deployment](#docker-production-deployment)
6. [SSL/TLS Configuration](#ssltls-configuration)
7. [Stripe Configuration](#stripe-configuration)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Server**: Ubuntu 20.04+ LTS or similar Linux distribution
- **RAM**: Minimum 4GB (8GB recommended for production)
- **CPU**: 2+ cores recommended
- **Storage**: 20GB+ available disk space
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+

### External Services Required

1. **Stripe Account** (for payments)
   - Create account at https://stripe.com
   - Set up products and pricing
   - Configure webhooks

2. **OpenAI API** (for AI caption generation)
   - Create account at https://platform.openai.com
   - Generate API key

3. **AWS S3** (for media storage)
   - Create S3 bucket
   - Configure IAM user with S3 access

4. **Instagram App** (for Instagram integration)
   - Create app at https://developers.facebook.com
   - Configure OAuth redirects

5. **Domain Name** (recommended)
   - Point A/AAAA records to your server IP
   - Configure DNS for your domain

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Pyralys.git
cd Pyralys
```

### 2. Install Docker & Docker Compose

```bash
# Update package list
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Configure Firewall

```bash
# Allow SSH (if not already configured)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

## Database Migrations

### Setup Alembic Migrations

The project includes Alembic migrations for database schema management.

#### Run Migrations in Docker

```bash
# Start only the database
docker-compose -f docker-compose.prod.yml up -d postgres

# Wait for database to be ready (check with docker logs)
docker logs pyralys-postgres-prod

# Run migrations
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head
```

#### Create New Migrations (Development)

```bash
# After modifying models, generate migration
docker-compose run --rm backend alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file in backend/alembic/versions/

# Apply migration
docker-compose run --rm backend alembic upgrade head
```

#### Migration Commands

```bash
# Show current migration version
alembic current

# Show migration history
alembic history

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Upgrade to latest
alembic upgrade head
```

## Environment Configuration

### 1. Backend Configuration

```bash
# Copy template
cp .env.production.template backend/.env.production

# Edit with your actual values
nano backend/.env.production
```

**Critical values to configure:**

```env
# Strong passwords (generate with: openssl rand -hex 32)
POSTGRES_PASSWORD=<strong-random-password>
REDIS_PASSWORD=<strong-random-password>
SECRET_KEY=<random-secret-key>
JWT_SECRET_KEY=<random-jwt-secret>

# Stripe (use live keys, not test keys)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# OpenAI
OPENAI_API_KEY=sk-...

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET_NAME=pyralys-production-media

# Instagram
INSTAGRAM_APP_ID=...
INSTAGRAM_APP_SECRET=...
INSTAGRAM_REDIRECT_URI=https://yourdomain.com/api/v1/auth/instagram/callback

# URLs
FRONTEND_URL=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com
```

### 2. Frontend Configuration

```bash
# Create frontend production env
nano frontend/.env.production
```

```env
NEXT_PUBLIC_API_URL=https://yourdomain.com/api/v1
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_INSTAGRAM_APP_ID=...
```

### 3. Root Environment File

```bash
# Create .env file for Docker Compose
nano .env.production
```

```env
POSTGRES_USER=pyralys_prod
POSTGRES_PASSWORD=<same-as-backend>
POSTGRES_DB=pyralys_production
REDIS_PASSWORD=<same-as-backend>
NEXT_PUBLIC_API_URL=https://yourdomain.com/api/v1
```

## Docker Production Deployment

### 1. Build Images

```bash
# Build all production images
docker-compose -f docker-compose.prod.yml build

# Or build specific service
docker-compose -f docker-compose.prod.yml build backend
```

### 2. Start Services

```bash
# Start all services in detached mode
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# View logs for specific service
docker-compose -f docker-compose.prod.yml logs -f backend
```

### 3. Verify Deployment

```bash
# Check backend health
curl http://localhost/api/v1/health

# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Should show all services as "Up"
```

### 4. Create Initial Admin User (Optional)

```bash
# Access backend container
docker-compose -f docker-compose.prod.yml exec backend bash

# Run Python shell
python

# Create admin user
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@yourdomain.com",
    hashed_password=get_password_hash("secure-password-here"),
    full_name="Admin User",
    plan_type="enterprise"
)
db.add(admin)
db.commit()
exit()
```

## SSL/TLS Configuration

### Option 1: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Stop nginx container temporarily
docker-compose -f docker-compose.prod.yml stop nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to nginx directory
sudo mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/

# Update nginx.conf to enable SSL (uncomment SSL sections)
nano nginx/nginx.conf

# Restart nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

### Option 2: Custom SSL Certificate

```bash
# Place your certificates in nginx/ssl/
mkdir -p nginx/ssl
cp your-fullchain.pem nginx/ssl/fullchain.pem
cp your-privkey.pem nginx/ssl/privkey.pem

# Update nginx.conf
nano nginx/nginx.conf
# Uncomment SSL configuration lines and update server_name

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Auto-renewal (Let's Encrypt)

```bash
# Add to crontab
sudo crontab -e

# Add this line to check for renewal twice daily
0 0,12 * * * certbot renew --quiet && docker-compose -f /path/to/Pyralys/docker-compose.prod.yml restart nginx
```

## Stripe Configuration

### 1. Create Products and Prices

1. Go to Stripe Dashboard → Products
2. Create products:
   - **Premium**: $19.99/month
   - **Pro**: $49.99/month
   - **Enterprise**: $99.99/month

3. Copy the Price IDs and update `backend/.env.production`:

```env
STRIPE_PRICE_PREMIUM=price_xxxxx
STRIPE_PRICE_PRO=price_xxxxx
STRIPE_PRICE_ENTERPRISE=price_xxxxx
```

4. Update `backend/app/services/stripe_service.py` with the correct price IDs

### 2. Configure Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Click "Add endpoint"
3. Set endpoint URL: `https://yourdomain.com/api/v1/billing/webhooks/stripe`
4. Select events to listen for:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`

5. Copy the webhook signing secret and update `.env.production`:

```env
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

### 3. Test Webhook

```bash
# Install Stripe CLI
curl -s https://packages.stripe.com/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.com/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
sudo apt update
sudo apt install stripe

# Forward webhooks to local
stripe listen --forward-to https://yourdomain.com/api/v1/billing/webhooks/stripe

# Test a webhook
stripe trigger customer.subscription.created
```

## Monitoring & Maintenance

### Health Checks

```bash
# Check all services
docker-compose -f docker-compose.prod.yml ps

# Backend health endpoint
curl https://yourdomain.com/health

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
docker-compose -f docker-compose.prod.yml logs --tail=100 celery_worker
```

### Celery Monitoring (Flower)

Flower is included for Celery task monitoring, but should NOT be exposed publicly in production.

To access Flower:

1. SSH into your server with port forwarding:
```bash
ssh -L 5555:localhost:5555 user@yourserver
```

2. Access Flower at `http://localhost:5555` in your browser

### Database Backups

```bash
# Create backup script
nano /usr/local/bin/backup-pyralys.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backups/pyralys"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec pyralys-postgres-prod pg_dump -U pyralys_prod pyralys_production | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Backup Redis (if needed)
docker exec pyralys-redis-prod redis-cli --pass YOUR_REDIS_PASSWORD SAVE
docker cp pyralys-redis-prod:/data/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# Make executable
chmod +x /usr/local/bin/backup-pyralys.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /usr/local/bin/backup-pyralys.sh >> /var/log/pyralys-backup.log 2>&1
```

### Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/pyralys
```

```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nginx adm
    sharedscripts
    postrotate
        docker-compose -f /path/to/Pyralys/docker-compose.prod.yml exec nginx nginx -s reload
    endscript
}
```

### Updates and Upgrades

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose -f docker-compose.prod.yml build

# Run migrations
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head

# Restart services (zero-downtime with rolling restart)
docker-compose -f docker-compose.prod.yml up -d --no-deps --build backend
docker-compose -f docker-compose.prod.yml up -d --no-deps --build frontend
docker-compose -f docker-compose.prod.yml restart celery_worker celery_beat
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check specific service
docker-compose -f docker-compose.prod.yml logs backend

# Restart all services
docker-compose -f docker-compose.prod.yml restart

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.prod.yml ps postgres

# Check PostgreSQL logs
docker-compose -f docker-compose.prod.yml logs postgres

# Test connection from backend
docker-compose -f docker-compose.prod.yml exec backend bash
python -c "from app.core.database import engine; print('OK')"
```

### Celery Tasks Not Running

```bash
# Check Celery worker logs
docker-compose -f docker-compose.prod.yml logs celery_worker

# Check Redis connection
docker-compose -f docker-compose.prod.yml exec redis redis-cli --pass YOUR_PASSWORD ping

# Restart Celery services
docker-compose -f docker-compose.prod.yml restart celery_worker celery_beat
```

### High Memory Usage

```bash
# Check resource usage
docker stats

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# Clear Redis cache
docker-compose -f docker-compose.prod.yml exec redis redis-cli --pass YOUR_PASSWORD FLUSHDB
```

### 502 Bad Gateway

```bash
# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx

# Check backend is running
docker-compose -f docker-compose.prod.yml ps backend

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

## Security Best Practices

1. **Never expose database ports publicly**
   - PostgreSQL (5432) and Redis (6379) should only be accessible within Docker network

2. **Use strong passwords**
   - Generate with: `openssl rand -hex 32`

3. **Keep secrets secure**
   - Never commit `.env` files
   - Use environment variables or secrets manager

4. **Enable SSL/TLS**
   - Always use HTTPS in production
   - Configure HSTS headers

5. **Regular updates**
   - Keep Docker images updated
   - Update dependencies regularly
   - Apply security patches

6. **Rate limiting**
   - Nginx config includes rate limiting
   - Monitor for abuse

7. **Backup regularly**
   - Automated daily backups
   - Test restore procedures

8. **Monitor logs**
   - Set up log aggregation
   - Configure alerts for errors

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/Pyralys/issues
- Documentation: https://docs.pyralys.com

---

**Last Updated**: January 2025
