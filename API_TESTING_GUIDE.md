# Pyralys API Testing Guide

Comprehensive guide for testing all Pyralys API endpoints.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [Content Management](#content-management)
4. [AI Generation](#ai-generation)
5. [Publishing & Scheduling](#publishing--scheduling)
6. [Analytics](#analytics)
7. [Billing & Subscriptions](#billing--subscriptions)
8. [Social Accounts](#social-accounts)
9. [Monitoring](#monitoring)

## Getting Started

### Base URL

**Development:**
```
http://localhost:8000/api/v1
```

**Production:**
```
https://yourdomain.com/api/v1
```

### Authentication

Most endpoints require authentication via JWT token. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Testing Tools

**Recommended:**
- [Postman](https://www.postman.com/) - GUI API client
- [HTTPie](https://httpie.io/) - Command-line HTTP client
- [curl](https://curl.se/) - Command-line tool
- [Thunder Client](https://www.thunderclient.com/) - VS Code extension

## Authentication

### 1. Health Check

Check API health status.

```bash
# Request
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00"
}
```

### 2. Register User

Create a new user account.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
  }'

# Response
{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "plan_type": "free",
  "created_at": "2025-01-01T12:00:00"
}
```

### 3. Login

Authenticate and receive JWT tokens.

```bash
# Request (Form data)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePassword123!"

# Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 4. Refresh Token

Get a new access token using refresh token.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "your-refresh-token-here"
  }'

# Response
{
  "access_token": "new-access-token",
  "token_type": "bearer"
}
```

### 5. Get Current User

Get authenticated user profile.

```bash
# Request
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "plan_type": "free",
  "created_at": "2025-01-01T12:00:00"
}
```

## Content Management

### 1. Create Post

Create a new post.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/content \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "caption": "This is an amazing caption! #ai #socialmedia",
    "platform": "instagram",
    "media_urls": ["https://example.com/image.jpg"],
    "scheduled_at": "2025-01-02T14:00:00"
  }'

# Response
{
  "id": "post-uuid",
  "title": "My First Post",
  "caption": "This is an amazing caption!",
  "platform": "instagram",
  "status": "draft",
  "scheduled_at": "2025-01-02T14:00:00",
  "created_at": "2025-01-01T12:00:00"
}
```

### 2. List Posts

Get all posts for the authenticated user.

```bash
# Request
curl http://localhost:8000/api/v1/content?skip=0&limit=20 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Query Parameters:
# - skip: Number of posts to skip (pagination)
# - limit: Number of posts to return (max 100)
# - status: Filter by status (draft, scheduled, published, failed)
# - platform: Filter by platform (instagram, wordpress)

# Response
[
  {
    "id": "uuid",
    "title": "Post Title",
    "caption": "Caption text",
    "platform": "instagram",
    "status": "published",
    "published_at": "2025-01-01T15:00:00"
  }
]
```

### 3. Get Post by ID

Retrieve a specific post.

```bash
# Request
curl http://localhost:8000/api/v1/content/{post_id} \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "id": "post-uuid",
  "title": "Post Title",
  "caption": "Full caption text",
  "media_urls": ["url1", "url2"],
  "platform": "instagram",
  "status": "published",
  "likes_count": 150,
  "comments_count": 25,
  "reach": 5000,
  "engagement_rate": 3.5
}
```

### 4. Update Post

Update an existing post.

```bash
# Request
curl -X PUT http://localhost:8000/api/v1/content/{post_id} \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "caption": "Updated caption text"
  }'

# Response
{
  "id": "post-uuid",
  "title": "Updated Title",
  "caption": "Updated caption text",
  "updated_at": "2025-01-01T13:00:00"
}
```

### 5. Delete Post

Delete a post.

```bash
# Request
curl -X DELETE http://localhost:8000/api/v1/content/{post_id} \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "message": "Post deleted successfully"
}
```

## AI Generation

### 1. Generate Caption

Generate AI-powered caption for Instagram.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/ai/generate/caption \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "summer vacation at the beach",
    "tone": "casual",
    "platform": "instagram",
    "length": "medium",
    "include_hashtags": true,
    "include_emoji": true
  }'

# Response
{
  "caption": "Summer vibes hitting different at the beach! 🏖️☀️ Nothing beats the sound of waves and feeling sand between your toes. Who else is ready for vacation season? #SummerVibes #BeachLife #VacationMode",
  "hashtags": ["#SummerVibes", "#BeachLife", "#VacationMode"],
  "model_used": "gpt-4-turbo",
  "tokens_used": 150
}
```

### 2. Generate Hashtags

Generate relevant hashtags.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/ai/generate/hashtags \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Delicious homemade pasta recipe",
    "platform": "instagram",
    "count": 10
  }'

# Response
{
  "hashtags": [
    "#PastaRecipe",
    "#Homemade",
    "#ItalianFood",
    "#Foodie",
    "#CookingAtHome"
  ],
  "relevance_scores": [0.95, 0.92, 0.88, 0.85, 0.82]
}
```

### 3. Generate Image

Generate AI image using DALL-E.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/ai/generate/image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Sunset over mountains, vibrant colors, professional photography",
    "size": "1024x1024",
    "style": "vivid",
    "quality": "hd"
  }'

# Response
{
  "image_url": "https://cdn.example.com/generated-image.jpg",
  "prompt": "Sunset over mountains...",
  "model": "dall-e-3",
  "revised_prompt": "A stunning sunset...",
  "created_at": "2025-01-01T12:00:00"
}
```

## Publishing & Scheduling

### 1. Publish Post

Publish a post immediately to a platform.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/content/{post_id}/publish \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["instagram"],
    "publish_now": true
  }'

# Response
{
  "task_id": "celery-task-uuid",
  "message": "Post queued for publishing",
  "status": "pending"
}
```

### 2. Schedule Post

Schedule a post for future publication.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/content/{post_id}/schedule \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scheduled_at": "2025-01-05T10:00:00",
    "platforms": ["instagram", "wordpress"]
  }'

# Response
{
  "message": "Post scheduled successfully",
  "scheduled_at": "2025-01-05T10:00:00",
  "platforms": ["instagram", "wordpress"]
}
```

### 3. Cancel Scheduled Post

Cancel a scheduled post.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/content/{post_id}/cancel \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "message": "Scheduled post cancelled",
  "status": "draft"
}
```

### 4. Get Task Status

Check status of a publishing task.

```bash
# Request
curl http://localhost:8000/api/v1/monitoring/tasks/{task_id} \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "task_id": "uuid",
  "state": "SUCCESS",
  "result": {
    "platform_post_id": "instagram-post-id",
    "url": "https://instagram.com/p/..."
  },
  "progress": 100
}
```

## Analytics

### 1. Get Dashboard Overview

Get complete analytics dashboard data.

```bash
# Request
curl http://localhost:8000/api/v1/analytics/dashboard?days=30 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Query Parameters:
# - days: Time period (7, 30, 90)

# Response
{
  "overview": {
    "total_posts": 45,
    "total_engagement": 12500,
    "total_reach": 50000,
    "total_impressions": 75000
  },
  "platform_performance": [
    {
      "platform": "instagram",
      "posts_count": 30,
      "avg_engagement": 250,
      "success_rate": 95.5
    }
  ],
  "top_posts": [...],
  "growth_metrics": {...},
  "timeline": [...]
}
```

### 2. Get Platform Performance

Get analytics for specific platforms.

```bash
# Request
curl http://localhost:8000/api/v1/analytics/performance?days=30 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
[
  {
    "platform": "instagram",
    "posts_count": 30,
    "total_likes": 5000,
    "total_comments": 500,
    "avg_engagement_rate": 3.2,
    "success_rate": 95.0
  }
]
```

### 3. Get Top Posts

Retrieve best performing posts.

```bash
# Request
curl "http://localhost:8000/api/v1/analytics/top-posts?limit=10&metric=engagement" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Query Parameters:
# - limit: Number of posts (default 10)
# - metric: engagement | reach | impressions

# Response
[
  {
    "id": "post-uuid",
    "title": "Top Post",
    "platform": "instagram",
    "engagement_rate": 5.2,
    "likes_count": 500,
    "comments_count": 50,
    "published_at": "2025-01-01T10:00:00"
  }
]
```

### 4. Get Growth Metrics

Get period-over-period growth metrics.

```bash
# Request
curl http://localhost:8000/api/v1/analytics/growth?days=30 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "current_period": {
    "posts": 30,
    "engagement": 5000,
    "reach": 20000
  },
  "previous_period": {
    "posts": 25,
    "engagement": 4000,
    "reach": 15000
  },
  "growth": {
    "posts": 20.0,
    "engagement": 25.0,
    "reach": 33.3
  }
}
```

## Billing & Subscriptions

### 1. Get Available Plans

List all subscription plans.

```bash
# Request
curl http://localhost:8000/api/v1/billing/plans

# Response
{
  "plans": [
    {
      "name": "Free",
      "price": 0,
      "currency": "usd",
      "interval": "month",
      "features": [
        "10 AI captions per month",
        "Basic analytics",
        "1 social platform"
      ],
      "caption_limit": 10,
      "post_limit": 10
    },
    {
      "name": "Premium",
      "price": 1999,
      "currency": "usd",
      "interval": "month",
      "features": [...]
    }
  ]
}
```

### 2. Get Current Subscription

Get user's current subscription.

```bash
# Request
curl http://localhost:8000/api/v1/billing/subscription \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "id": "sub-uuid",
  "plan_type": "premium",
  "status": "active",
  "current_period_end": "2025-02-01T00:00:00",
  "cancel_at_period_end": false,
  "stripe_subscription_id": "sub_xxx"
}
```

### 3. Create Checkout Session

Create Stripe checkout for upgrading.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/billing/create-checkout \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "premium"
  }'

# Response
{
  "session_id": "cs_test_xxx",
  "url": "https://checkout.stripe.com/c/pay/cs_test_xxx"
}
```

### 4. Create Portal Session

Create Stripe Customer Portal session.

```bash
# Request
curl -X POST http://localhost:8000/api/v1/billing/create-portal \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "url": "https://billing.stripe.com/p/session/xxx"
}
```

### 5. Get Invoices

List user's invoices.

```bash
# Request
curl http://localhost:8000/api/v1/billing/invoices \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
[
  {
    "id": "inv-uuid",
    "amount_paid": 1999,
    "currency": "usd",
    "status": "paid",
    "invoice_date": "2025-01-01T00:00:00",
    "hosted_invoice_url": "https://invoice.stripe.com/i/xxx",
    "invoice_pdf": "https://invoice.stripe.com/i/xxx/pdf"
  }
]
```

## Social Accounts

### 1. Connect Instagram

Initiate Instagram OAuth flow.

```bash
# Request
curl http://localhost:8000/api/v1/auth/instagram/connect \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "authorization_url": "https://api.instagram.com/oauth/authorize?..."
}
```

### 2. List Connected Accounts

Get all connected social accounts.

```bash
# Request
curl http://localhost:8000/api/v1/social/accounts \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
[
  {
    "id": "account-uuid",
    "platform": "instagram",
    "username": "@johndoe",
    "is_active": true,
    "connected_at": "2025-01-01T12:00:00"
  }
]
```

## Monitoring

### 1. Get Workers Status

Check Celery workers health.

```bash
# Request
curl http://localhost:8000/api/v1/monitoring/workers \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "workers": [
    {
      "name": "worker@hostname",
      "status": "online",
      "processed": 1250,
      "active": 2
    }
  ]
}
```

### 2. Get Queue Status

Check task queue status.

```bash
# Request
curl http://localhost:8000/api/v1/monitoring/queues \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response
{
  "queues": [
    {
      "name": "celery",
      "messages": 5,
      "consumers": 4
    }
  ]
}
```

## Error Handling

All endpoints return errors in a consistent format:

```json
{
  "detail": "Error message here",
  "status_code": 400
}
```

### Common HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Missing or invalid auth token
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **422 Unprocessable Entity** - Validation error
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error

## Rate Limiting

**API Limits:**
- General endpoints: 30 requests/second
- AI generation: 10 requests/second
- Authentication: 5 requests/second

**Headers:**
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1640000000
```

## Testing Checklist

### Authentication Flow
- [ ] Register new user
- [ ] Login with credentials
- [ ] Refresh access token
- [ ] Access protected endpoint
- [ ] Handle expired token

### Content Management
- [ ] Create post
- [ ] List posts with pagination
- [ ] Update post
- [ ] Delete post
- [ ] Filter by status/platform

### AI Generation
- [ ] Generate caption
- [ ] Generate hashtags
- [ ] Generate image
- [ ] Check usage limits

### Publishing
- [ ] Publish immediately
- [ ] Schedule for later
- [ ] Cancel scheduled post
- [ ] Monitor task status

### Analytics
- [ ] Get dashboard overview
- [ ] View platform performance
- [ ] Check top posts
- [ ] Review growth metrics

### Billing
- [ ] View plans
- [ ] Check subscription
- [ ] Create checkout
- [ ] View invoices

## Automated Testing

### Using Postman

1. Import collection from `/tests/postman/pyralys-api.json`
2. Set environment variables (base_url, access_token)
3. Run collection tests

### Using pytest

```bash
cd backend
pytest tests/ -v --cov=app
```

### Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_auth.py -v
```

---

**Need Help?**

- API Documentation: http://localhost:8000/docs
- Issues: https://github.com/westekey/Pyralys/issues
- Support: support@pyralys.com
