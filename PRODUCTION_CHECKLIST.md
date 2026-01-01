# Production Deployment Checklist

Use this checklist to ensure a smooth production deployment of Pyralys.

## Pre-Deployment

### Infrastructure

- [ ] Server provisioned (4GB+ RAM, 2+ CPU cores, 20GB+ storage)
- [ ] Docker and Docker Compose installed
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] Domain name configured with DNS records pointing to server
- [ ] SSL certificate obtained (Let's Encrypt or custom)

### External Services

- [ ] Stripe account created and verified
- [ ] Stripe products created (Premium, Pro, Enterprise)
- [ ] Stripe price IDs copied
- [ ] Stripe webhook endpoint configured
- [ ] OpenAI API key obtained
- [ ] AWS account created
- [ ] S3 bucket created and configured
- [ ] IAM user created with S3 access
- [ ] Instagram App created at Facebook Developers
- [ ] Instagram OAuth configured
- [ ] SendGrid account created (for emails)

### Configuration Files

- [ ] `.env.production` created from template in backend/
- [ ] `.env.production` created in frontend/
- [ ] `.env.production` created in project root
- [ ] All passwords generated with strong randomness
- [ ] All API keys configured correctly
- [ ] Frontend URL configured
- [ ] Backend URL configured
- [ ] CORS origins configured
- [ ] Stripe price IDs updated in `stripe_service.py`

### Security Review

- [ ] Strong database password set
- [ ] Strong Redis password set
- [ ] JWT secret keys generated
- [ ] No `.env` files committed to git
- [ ] No test/development keys in production config
- [ ] Firewall rules reviewed
- [ ] SSL/TLS certificates valid
- [ ] Rate limiting configured in nginx
- [ ] Database ports NOT exposed publicly
- [ ] Redis port NOT exposed publicly

## Deployment

### Database Setup

- [ ] PostgreSQL container started
- [ ] Database created
- [ ] Alembic migrations run successfully
- [ ] Initial admin user created (optional)
- [ ] Database connection tested

### Application Deployment

- [ ] Docker images built successfully
- [ ] All containers started
- [ ] Health checks passing
- [ ] Backend API responding at `/health`
- [ ] Frontend loading correctly
- [ ] Nginx reverse proxy working
- [ ] HTTPS redirect working (if configured)
- [ ] API accessible through Nginx

### Celery & Background Tasks

- [ ] Celery worker started
- [ ] Celery beat scheduler started
- [ ] Redis connection working
- [ ] Test task executed successfully
- [ ] Flower monitoring accessible (via SSH tunnel)

### Stripe Integration

- [ ] Webhook endpoint accessible
- [ ] Webhook signature verification working
- [ ] Test subscription created successfully
- [ ] Test payment processed
- [ ] Invoice generation working
- [ ] Customer portal accessible

### Instagram Integration

- [ ] OAuth callback URL configured
- [ ] Test Instagram account connection
- [ ] Token refresh working
- [ ] Test post publishing
- [ ] Analytics collection working

### Email Configuration

- [ ] SendGrid API key configured
- [ ] Test email sent successfully
- [ ] Email templates working

## Post-Deployment

### Monitoring Setup

- [ ] Log rotation configured
- [ ] Database backup script created
- [ ] Backup cron job scheduled
- [ ] SSL certificate auto-renewal configured
- [ ] Health check monitoring set up
- [ ] Error alerting configured (optional)
- [ ] Uptime monitoring configured (optional)

### Testing

- [ ] User registration working
- [ ] User login working
- [ ] JWT token refresh working
- [ ] AI caption generation working
- [ ] Image generation working (if applicable)
- [ ] Instagram OAuth flow working
- [ ] WordPress connection working
- [ ] Post creation working
- [ ] Post publishing working (Instagram)
- [ ] Post publishing working (WordPress)
- [ ] Scheduled posts working
- [ ] Analytics dashboard loading
- [ ] Billing page loading
- [ ] Stripe checkout working
- [ ] Stripe customer portal working
- [ ] Webhook processing working
- [ ] Email notifications working

### Performance

- [ ] Response times acceptable (< 500ms for most endpoints)
- [ ] Database queries optimized
- [ ] Static assets cached properly
- [ ] Gzip compression working
- [ ] CDN configured (optional)
- [ ] Image optimization working

### Documentation

- [ ] Deployment documentation reviewed
- [ ] Team trained on deployment process
- [ ] Runbook created for common issues
- [ ] Backup restore procedure documented
- [ ] Emergency contacts documented

## Go-Live

- [ ] Final smoke test completed
- [ ] All team members notified
- [ ] Monitoring dashboards open
- [ ] Support channels ready
- [ ] Rollback plan prepared

## Post-Launch (First 24 Hours)

- [ ] Monitor error logs
- [ ] Check background task execution
- [ ] Verify scheduled tasks running
- [ ] Monitor resource usage (CPU, RAM, disk)
- [ ] Check email delivery
- [ ] Monitor Stripe webhook processing
- [ ] Verify database backups running
- [ ] Test critical user flows

## Weekly Maintenance

- [ ] Review error logs
- [ ] Check database growth
- [ ] Verify backups successful
- [ ] Review resource usage trends
- [ ] Update dependencies (security patches)
- [ ] Test backup restoration
- [ ] Review Celery task queue

## Monthly Maintenance

- [ ] Security updates applied
- [ ] SSL certificate expiry checked
- [ ] Database optimization (VACUUM, ANALYZE)
- [ ] Review and archive old logs
- [ ] Capacity planning review
- [ ] Disaster recovery drill
- [ ] Performance benchmarking

---

## Rollback Procedure

If critical issues occur after deployment:

1. **Stop accepting new traffic**
   ```bash
   # Stop frontend to prevent new user actions
   docker-compose -f docker-compose.prod.yml stop frontend nginx
   ```

2. **Identify the issue**
   - Check logs: `docker-compose -f docker-compose.prod.yml logs`
   - Check Sentry/monitoring tools
   - Check database state

3. **Roll back code**
   ```bash
   git checkout <previous-stable-tag>
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Roll back database** (if migration caused issue)
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend alembic downgrade -1
   ```

5. **Restore from backup** (if data corruption)
   ```bash
   # Stop services
   docker-compose -f docker-compose.prod.yml down

   # Restore database
   gunzip < /backups/pyralys/postgres_YYYYMMDD.sql.gz | \
     docker exec -i pyralys-postgres-prod psql -U pyralys_prod pyralys_production

   # Restart services
   docker-compose -f docker-compose.prod.yml up -d
   ```

6. **Verify functionality**
   - Test critical user flows
   - Check health endpoints
   - Monitor logs

7. **Communicate**
   - Notify users of the issue and resolution
   - Document the incident
   - Create post-mortem

---

**Notes:**
- Check items off as you complete them
- Don't skip security items
- Test everything in staging first
- Keep this checklist updated as process evolves
