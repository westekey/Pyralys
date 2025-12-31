# 🚀 Plan de Développement MVP - Pyralys

## Table des Matières
1. [Définition du MVP](#1-définition-du-mvp)
2. [Features Prioritized (MoSCoW)](#2-features-prioritized-moscow)
3. [Sprint Planning (8 semaines)](#3-sprint-planning-8-semaines)
4. [Stack Technique Setup](#4-stack-technique-setup)
5. [Implémentation Par Module](#5-implémentation-par-module)
6. [Testing Strategy](#6-testing-strategy)
7. [Deployment Plan](#7-deployment-plan)

---

## 1. Définition du MVP

### Vision MVP
**"Permettre à un utilisateur de générer un post Instagram avec IA (texte + image), le programmer, et voir ses performances de base en moins de 10 minutes."**

### Scope MVP (Ce qui EST inclus)

✅ **Authentication & Users**
- Inscription email/password
- Login JWT
- Password reset
- Profil utilisateur basique

✅ **Social Accounts**
- Connexion Instagram (OAuth)
- Gestion tokens Instagram

✅ **AI Content Generation**
- Génération caption avec GPT-4
- Génération hashtags optimisés
- Génération image avec DALL-E 3
- Preview multi-format (Feed, Story concept)

✅ **Content Management**
- CRUD posts (drafts)
- Upload images manuelles (alternative à AI)
- Scheduling avec date/time picker
- Publication Instagram Feed

✅ **Analytics Basiques**
- Fetch Instagram insights (likes, comments, reach)
- Dashboard avec métriques clés (derniers 30 jours)
- Performance par post (table)

✅ **Billing**
- Intégration Stripe (subscriptions)
- 2 plans : Free (limited) + Pro
- Gestion quotas

### Scope MVP (Ce qui N'EST PAS inclus)

❌ **Plateformes supplémentaires**
- TikTok, Facebook, LinkedIn, YouTube (Phase 2)

❌ **Features avancées**
- Génération vidéo
- Templates personnalisés
- A/B testing
- Analytics prédictifs ML
- Marketplace templates
- API publique
- White-label

❌ **Optimisations**
- Mobile app native
- Dark mode
- Internationalisation (EN uniquement MVP)
- Notifications push

---

## 2. Features Prioritized (MoSCoW)

### MUST Have (Critique pour MVP)

| Feature | Description | Effort | Valeur |
|---------|-------------|--------|--------|
| **User Auth** | Signup, Login, JWT | 3 days | Critique |
| **Instagram OAuth** | Connect IG account | 2 days | Critique |
| **AI Caption Generation** | GPT-4 integration | 3 days | Haute |
| **AI Image Generation** | DALL-E 3 integration | 2 days | Haute |
| **Post CRUD** | Create, Read, Update, Delete drafts | 4 days | Critique |
| **Instagram Publishing** | Post to IG via API | 3 days | Critique |
| **Scheduling System** | Celery queue for timed posts | 3 days | Haute |
| **Basic Analytics** | Fetch IG insights + display | 4 days | Haute |
| **Dashboard UI** | Stats overview + recent posts | 5 days | Haute |
| **Content Studio UI** | Generation + preview interface | 6 days | Critique |
| **Stripe Billing** | Subscription payments | 3 days | Haute |

**Total MUST Have : ~38 jours-dev**

### SHOULD Have (Important mais pas bloquant)

| Feature | Description | Effort | Valeur |
|---------|-------------|--------|--------|
| **AI Prediction Score** | Estimate post performance | 4 days | Moyenne |
| **Optimal Time Suggestion** | Best time to post based on data | 3 days | Moyenne |
| **Hashtag Recommender** | Smart hashtag suggestions | 2 days | Moyenne |
| **Post Templates** | 5-10 templates pré-faits | 3 days | Moyenne |
| **Email Notifications** | Post published, analytics digest | 2 days | Faible |
| **User Onboarding Flow** | Guided first experience | 3 days | Moyenne |

**Total SHOULD Have : ~17 jours-dev**

### COULD Have (Nice-to-have)

| Feature | Description | Effort | Valeur |
|---------|-------------|--------|--------|
| **Brand Voice Learning** | Learn user's writing style | 5 days | Faible |
| **Image Filters** | Apply filters to AI images | 2 days | Faible |
| **Multi-Image Carousel** | Instagram carousel support | 3 days | Faible |
| **Dark Mode** | UI dark theme | 2 days | Faible |

### WON'T Have (Phase 2+)

- Vidéo generation
- TikTok, Facebook, LinkedIn
- Advanced analytics (ML predictions)
- Mobile app
- Zapier integration
- API publique

---

## 3. Sprint Planning (8 Semaines)

### Sprint 0 : Setup & Infrastructure (Semaine 1)

**Objectif :** Infrastructure prête pour développement

**Backend Tasks :**
- [ ] Setup repo GitHub + CI/CD
- [ ] Docker configuration (dev + prod)
- [ ] PostgreSQL database + migrations setup
- [ ] Redis setup
- [ ] FastAPI project structure
- [ ] Environment configuration (.env)
- [ ] AWS account setup (S3, RDS, ElastiCache)
- [ ] Terraform config basics

**Frontend Tasks :**
- [ ] Next.js project init
- [ ] Tailwind + shadcn/ui setup
- [ ] Folder structure + routing
- [ ] API client configuration (axios)
- [ ] Zustand stores setup
- [ ] Design system foundations (colors, fonts)

**DevOps Tasks :**
- [ ] GitHub Actions workflows
- [ ] Docker registry (ECR)
- [ ] Dev environment deployment

**Équipe :** 2 backend + 2 frontend + 0.5 DevOps
**Livrables :** Code skeleton, CI/CD running

---

### Sprint 1 : Authentication & Users (Semaine 2)

**Objectif :** Users can signup, login, manage profile

**Backend Tasks :**
- [ ] User model + DB schema
- [ ] Password hashing (bcrypt)
- [ ] JWT token generation/validation
- [ ] Register endpoint
- [ ] Login endpoint
- [ ] Refresh token endpoint
- [ ] Get current user endpoint
- [ ] Password reset (email flow avec SendGrid)
- [ ] Unit tests for auth

**Frontend Tasks :**
- [ ] Login page UI
- [ ] Register page UI
- [ ] Form validation (react-hook-form + zod)
- [ ] Auth context/store
- [ ] Protected routes HOC
- [ ] Profile page (view/edit)

**Endpoint Specs :**
```
POST   /api/v1/auth/register
  Body: { email, password, full_name }
  Response: { access_token, refresh_token, user }

POST   /api/v1/auth/login
  Body: { email, password }
  Response: { access_token, refresh_token, user }

POST   /api/v1/auth/refresh
  Body: { refresh_token }
  Response: { access_token }

GET    /api/v1/auth/me
  Headers: Authorization: Bearer {token}
  Response: { user }
```

**Tests :**
- [ ] Unit tests (pytest)
- [ ] E2E tests (Playwright)

**Équipe :** 1 backend + 1 frontend
**Livrables :** Working auth system

---

### Sprint 2 : Instagram OAuth & Accounts (Semaine 3)

**Objectif :** Users can connect their Instagram account

**Backend Tasks :**
- [ ] SocialAccount model + DB schema
- [ ] Instagram OAuth flow implementation
- [ ] Token storage (encrypted)
- [ ] Token refresh logic
- [ ] Instagram API client wrapper
- [ ] Get Instagram user info
- [ ] List connected accounts endpoint
- [ ] Disconnect account endpoint

**Frontend Tasks :**
- [ ] Connect Instagram button (OAuth redirect)
- [ ] OAuth callback handler
- [ ] Settings page (connected accounts)
- [ ] Account status indicators
- [ ] Reconnect flow if token expired

**Endpoint Specs :**
```
GET    /api/v1/social/instagram/auth-url
  Response: { auth_url }

GET    /api/v1/social/instagram/callback?code=xxx
  Response: { success, account }

GET    /api/v1/social/accounts
  Response: { accounts: [...] }

DELETE /api/v1/social/accounts/:id
  Response: { success }
```

**Tests :**
- [ ] Mock Instagram API responses
- [ ] Test OAuth flow

**Équipe :** 1 backend + 1 frontend
**Livrables :** Instagram account connection working

---

### Sprint 3 : AI Content Generation (Semaine 4)

**Objectif :** Generate captions and images with AI

**Backend Tasks :**
- [ ] OpenAI client integration
- [ ] Caption generation service
  - [ ] Prompt engineering for Instagram
  - [ ] Tone variations
  - [ ] Context handling
- [ ] Hashtag generation service
  - [ ] Mix popular + niche
  - [ ] Platform-specific limits
- [ ] Image generation service
  - [ ] DALL-E 3 integration
  - [ ] Image download + S3 upload
  - [ ] Error handling + retries
- [ ] Quota tracking (API costs)
- [ ] Caching strategy

**Frontend Tasks :**
- [ ] AI generation panel UI
- [ ] Prompt input (textarea + suggestions)
- [ ] Platform selector (chips)
- [ ] Tone selector (radio)
- [ ] Generate button (with loading state)
- [ ] Result preview
- [ ] Regenerate options
- [ ] Edit generated content

**Endpoint Specs :**
```
POST   /api/v1/ai/generate-caption
  Body: {
    prompt: string,
    platform: "instagram",
    tone: "casual" | "professional" | "funny" | "inspirational",
    user_context?: object
  }
  Response: {
    caption: string,
    hashtags: string[],
    metadata: object
  }

POST   /api/v1/ai/generate-image
  Body: {
    prompt: string,
    style?: string,
    size?: "1024x1024" | "1024x1792" | "1792x1024"
  }
  Response: {
    image_url: string,
    prompt_used: string
  }
```

**Optimisations :**
- [ ] Rate limiting (10 generations/minute)
- [ ] Cache responses (same prompt = same result for 1h)
- [ ] Background jobs for slow operations

**Tests :**
- [ ] Mock OpenAI API
- [ ] Test prompt variations
- [ ] Test error handling

**Équipe :** 1 backend + 1 frontend
**Livrables :** AI generation functional

---

### Sprint 4 : Content Management & Storage (Semaine 5)

**Objectif :** Users can create, save, edit drafts

**Backend Tasks :**
- [ ] Post model + DB schema
- [ ] CRUD endpoints
  - [ ] Create draft
  - [ ] List posts (with filters: draft, scheduled, published)
  - [ ] Get post by ID
  - [ ] Update post
  - [ ] Delete post
- [ ] Media upload handling
  - [ ] S3 upload endpoint
  - [ ] File validation (type, size)
  - [ ] Thumbnail generation
- [ ] Post status management (draft → scheduled → published)

**Frontend Tasks :**
- [ ] Content Studio main page
- [ ] Post creation flow
- [ ] Media upload (drag-drop + file picker)
- [ ] Draft save (auto-save)
- [ ] Post list view (table + cards)
- [ ] Post edit modal
- [ ] Delete confirmation

**Endpoint Specs :**
```
POST   /api/v1/content/posts
  Body: {
    title?: string,
    caption: string,
    media_urls: string[],
    platform: string,
    ai_generated: boolean,
    generation_params?: object
  }
  Response: { post }

GET    /api/v1/content/posts?status=draft&platform=instagram
  Response: { posts: [...], total, page }

GET    /api/v1/content/posts/:id
  Response: { post }

PUT    /api/v1/content/posts/:id
  Body: { caption?, media_urls?, ... }
  Response: { post }

DELETE /api/v1/content/posts/:id
  Response: { success }

POST   /api/v1/content/upload
  Body: FormData (file)
  Response: { url, thumbnail_url }
```

**Tests :**
- [ ] CRUD operations
- [ ] File upload validation
- [ ] Permissions (user can only edit their posts)

**Équipe :** 2 backend + 1 frontend
**Livrables :** Post management functional

---

### Sprint 5 : Scheduling & Publishing (Semaine 6)

**Objectif :** Users can schedule and publish to Instagram

**Backend Tasks :**
- [ ] Celery setup + worker configuration
- [ ] Scheduling endpoint
  - [ ] Validate scheduled time (not in past)
  - [ ] Create Celery task
  - [ ] Update post status
- [ ] Publishing service
  - [ ] Instagram Graph API integration
  - [ ] Image upload to Instagram
  - [ ] Caption + hashtags formatting
  - [ ] Error handling + retry logic
- [ ] Publish endpoint (immediate)
- [ ] Celery beat for scheduled tasks
- [ ] Webhook handler (Instagram notifications)

**Frontend Tasks :**
- [ ] Schedule modal
  - [ ] Calendar picker
  - [ ] Time picker
  - [ ] Timezone selector
- [ ] "Schedule" button
- [ ] "Publish Now" button
- [ ] Publishing status indicators
- [ ] Success/error notifications
- [ ] Calendar view (scheduled posts)

**Endpoint Specs :**
```
POST   /api/v1/content/posts/:id/schedule
  Body: { scheduled_at: ISO datetime }
  Response: { post, task_id }

POST   /api/v1/content/posts/:id/publish
  Response: { post, platform_post_id }

GET    /api/v1/content/calendar?start_date=xxx&end_date=xxx
  Response: { posts_by_date: {...} }
```

**Celery Tasks :**
```python
@celery_app.task(bind=True, max_retries=3)
def publish_instagram_post(self, post_id: str):
    # Implementation
    pass
```

**Tests :**
- [ ] Mock Instagram API
- [ ] Test scheduling logic
- [ ] Test retry mechanism
- [ ] Test webhook processing

**Équipe :** 2 backend + 1 frontend
**Livrables :** Publishing to Instagram works

---

### Sprint 6 : Analytics & Dashboard (Semaine 7)

**Objectif :** Users see basic analytics

**Backend Tasks :**
- [ ] PostMetrics model + TimescaleDB setup
- [ ] Fetch Instagram insights (Celery task)
  - [ ] Run every hour for recent posts
  - [ ] Store metrics in TimescaleDB
- [ ] Analytics aggregation queries
  - [ ] Total stats (last 7/30/90 days)
  - [ ] Performance by post
  - [ ] Engagement rate calculation
  - [ ] Trend calculations
- [ ] Analytics endpoints
- [ ] Dashboard stats endpoint

**Frontend Tasks :**
- [ ] Dashboard page
  - [ ] Stats cards (posts, likes, followers, engagement)
  - [ ] Performance chart (Recharts)
  - [ ] Top posts list
  - [ ] Recent activity
- [ ] Analytics page
  - [ ] Date range selector
  - [ ] Detailed charts
  - [ ] Export to CSV
- [ ] Post-specific analytics modal

**Endpoint Specs :**
```
GET    /api/v1/analytics/dashboard?period=30d
  Response: {
    total_posts: number,
    total_likes: number,
    total_comments: number,
    avg_engagement_rate: number,
    follower_growth: number,
    chart_data: [{ date, likes, comments, ... }]
  }

GET    /api/v1/analytics/posts/:id
  Response: {
    post,
    metrics: {
      impressions, reach, likes, comments, saves, shares,
      engagement_rate, performance_score
    },
    timeline: [{ timestamp, metric_name, value }]
  }

GET    /api/v1/analytics/export?format=csv&start_date=xxx
  Response: CSV file download
```

**Charts :**
- Line chart : Engagement over time
- Bar chart : Performance by post
- Pie chart : Platform distribution

**Tests :**
- [ ] Mock Instagram Insights API
- [ ] Test metrics calculations
- [ ] Test aggregation queries

**Équipe :** 1 backend + 2 frontend
**Livrables :** Analytics dashboard functional

---

### Sprint 7 : Billing & Quotas (Semaine 8)

**Objectif :** Users can subscribe to paid plans

**Backend Tasks :**
- [ ] Subscription model + DB schema
- [ ] Stripe integration
  - [ ] Create checkout session
  - [ ] Handle webhooks
  - [ ] Update user subscription status
- [ ] Quota management
  - [ ] Track AI generations
  - [ ] Track posts published
  - [ ] Enforce limits
- [ ] Billing endpoints

**Frontend Tasks :**
- [ ] Pricing page
- [ ] Checkout flow
- [ ] Billing settings page
  - [ ] Current plan
  - [ ] Usage stats
  - [ ] Upgrade/downgrade
  - [ ] Cancel subscription
- [ ] Quota indicators (header badge)

**Pricing Plans :**
```
FREE:
- 5 posts/month
- 10 AI generations/month
- 1 Instagram account
- Basic analytics

PRO ($49/month):
- Unlimited posts
- Unlimited AI generations
- 3 Instagram accounts
- Advanced analytics
- Priority support
```

**Endpoint Specs :**
```
POST   /api/v1/billing/create-checkout
  Body: { plan: "pro" }
  Response: { checkout_url }

POST   /api/v1/billing/webhooks/stripe
  Body: Stripe webhook payload
  Response: { received: true }

GET    /api/v1/billing/subscription
  Response: {
    plan: "free" | "pro",
    status: "active" | "cancelled",
    current_period_end: datetime,
    usage: { posts: 3, ai_generations: 7 }
  }

POST   /api/v1/billing/cancel-subscription
  Response: { success }
```

**Tests :**
- [ ] Mock Stripe API
- [ ] Test webhook handling
- [ ] Test quota enforcement

**Équipe :** 1 backend + 1 frontend
**Livrables :** Billing functional

---

### Sprint 8 : Polish, Testing & Deployment (Semaine 9)

**Objectif :** MVP production-ready

**Backend Tasks :**
- [ ] Security audit
  - [ ] SQL injection prevention
  - [ ] XSS prevention
  - [ ] CSRF tokens
  - [ ] Rate limiting
- [ ] Performance optimization
  - [ ] Database indexes
  - [ ] Query optimization
  - [ ] Caching strategy
- [ ] Error handling improvements
- [ ] Logging setup (structured logs)
- [ ] Monitoring (Sentry, Datadog)

**Frontend Tasks :**
- [ ] Responsive design fixes
- [ ] Cross-browser testing
- [ ] Accessibility audit (Lighthouse)
- [ ] Loading states polish
- [ ] Error boundaries
- [ ] SEO optimization (meta tags, sitemap)

**Testing :**
- [ ] Integration tests
- [ ] E2E tests (Playwright)
- [ ] Load testing (Locust)
- [ ] Security testing (OWASP ZAP)

**DevOps :**
- [ ] Production environment setup
  - [ ] AWS ECS Fargate
  - [ ] RDS PostgreSQL (production)
  - [ ] ElastiCache Redis
  - [ ] S3 buckets
  - [ ] CloudFront CDN
- [ ] SSL certificates
- [ ] Domain configuration
- [ ] Monitoring dashboards
- [ ] Backup strategy

**Documentation :**
- [ ] API documentation (OpenAPI/Swagger)
- [ ] User guide
- [ ] Admin runbook

**Équipe :** 2 backend + 2 frontend + 1 DevOps
**Livrables :** MVP en production

---

## 4. Stack Technique Setup

### Backend Dependencies (Python)

```txt
# requirements.txt

# Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Redis & Celery
redis==5.0.1
celery==5.3.6
flower==2.0.1

# Auth & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# AI & ML
openai==1.10.0
anthropic==0.10.0  # Alternative LLM
pillow==10.2.0

# Social APIs
requests==2.31.0
httpx==0.26.0

# Cloud & Storage
boto3==1.34.34  # AWS SDK
stripe==8.0.0

# Email
sendgrid==6.11.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
```

### Frontend Dependencies (Node.js)

```json
{
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",

    "@tanstack/react-query": "^5.17.19",
    "axios": "^1.6.5",
    "zustand": "^4.5.0",

    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",

    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",

    "recharts": "^2.10.4",
    "date-fns": "^3.2.0",
    "react-day-picker": "^8.10.0",

    "framer-motion": "^11.0.3",
    "react-hot-toast": "^2.4.1",

    "lucide-react": "^0.314.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.5",
    "@types/react": "^18.2.48",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "eslint": "^8.56.0",
    "eslint-config-next": "14.1.0",
    "prettier": "^3.2.4"
  }
}
```

---

## 5. Implémentation Par Module

### Module 1 : Authentication

**Backend Structure :**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── auth.py          # Auth routes
│   ├── core/
│   │   ├── config.py                # Settings
│   │   ├── security.py              # JWT, password hashing
│   │   └── dependencies.py          # FastAPI dependencies
│   ├── models/
│   │   └── user.py                  # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py                  # Pydantic schemas
│   └── services/
│       └── auth_service.py          # Business logic
```

**Exemple Implementation :**
```python
# app/core/security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, auth_service: AuthService = Depends()):
    user = await auth_service.create_user(user_data)
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, auth_service: AuthService = Depends()):
    user = await auth_service.authenticate(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user": user}
```

**Frontend Structure :**
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
├── components/
│   └── auth/
│       ├── LoginForm.tsx
│       └── RegisterForm.tsx
├── hooks/
│   └── useAuth.ts
└── lib/
    ├── api.ts                       # Axios instance
    └── auth.ts                      # Auth utilities
```

**Exemple Implementation :**
```tsx
// hooks/useAuth.ts
import { create } from 'zustand';
import { api } from '@/lib/api';

interface AuthStore {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuth = create<AuthStore>((set) => ({
  user: null,
  token: localStorage.getItem('token'),

  login: async (email, password) => {
    const { data } = await api.post('/auth/login', { email, password });
    localStorage.setItem('token', data.access_token);
    set({ user: data.user, token: data.access_token });
  },

  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null });
  }
}));

// components/auth/LoginForm.tsx
export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login } = useAuth();

  const onSubmit = async (data) => {
    try {
      await login(data.email, data.password);
      router.push('/dashboard');
    } catch (error) {
      toast.error('Invalid credentials');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('email', { required: true })} placeholder="Email" />
      <Input {...register('password', { required: true })} type="password" placeholder="Password" />
      <Button type="submit">Login</Button>
    </form>
  );
}
```

---

### Module 2 : AI Generation

**Backend :**
```python
# app/services/ai/text_generator.py
from openai import AsyncOpenAI

class TextGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_caption(
        self,
        prompt: str,
        platform: str = "instagram",
        tone: str = "casual"
    ) -> dict:
        system_prompts = {
            "casual": "You are a friendly social media expert...",
            "professional": "You are a professional brand copywriter...",
            "funny": "You are a witty and humorous content creator...",
            "inspirational": "You are an inspiring motivational speaker..."
        }

        completion = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompts[tone]},
                {"role": "user", "content": f"Create an {platform} caption for: {prompt}"}
            ],
            temperature=0.7,
            max_tokens=500
        )

        caption = completion.choices[0].message.content

        # Generate hashtags
        hashtags = await self.generate_hashtags(prompt, platform)

        return {
            "caption": caption,
            "hashtags": hashtags,
            "metadata": {"model": "gpt-4-turbo", "tone": tone}
        }

    async def generate_hashtags(self, topic: str, platform: str, count: int = 10) -> list[str]:
        # Implementation
        pass
```

**Frontend :**
```tsx
// components/content-studio/AIGenerationPanel.tsx
export function AIGenerationPanel({ onGenerated }) {
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('instagram');
  const [tone, setTone] = useState('casual');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const { data } = await api.post('/ai/generate-caption', {
        prompt,
        platform,
        tone
      });
      onGenerated(data);
      toast.success('Content generated!');
    } catch (error) {
      toast.error('Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>AI Content Generator</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <Textarea
          placeholder="Describe your product or topic..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={4}
        />

        <div>
          <Label>Platform</Label>
          <div className="flex gap-2 mt-2">
            <Chip
              selected={platform === 'instagram'}
              onClick={() => setPlatform('instagram')}
            >
              Instagram
            </Chip>
            {/* More platforms */}
          </div>
        </div>

        <div>
          <Label>Tone</Label>
          <RadioGroup value={tone} onValueChange={setTone}>
            <RadioGroupItem value="casual">😎 Casual</RadioGroupItem>
            <RadioGroupItem value="professional">👔 Professional</RadioGroupItem>
            <RadioGroupItem value="funny">😂 Funny</RadioGroupItem>
          </RadioGroup>
        </div>

        <Button
          onClick={handleGenerate}
          disabled={!prompt || isGenerating}
          className="w-full"
        >
          {isGenerating ? 'Generating...' : '✨ Generate Content'}
        </Button>
      </CardContent>
    </Card>
  );
}
```

---

## 6. Testing Strategy

### Backend Tests

**Unit Tests (pytest) :**
```python
# tests/test_auth.py
import pytest
from app.core.security import verify_password, get_password_hash

def test_password_hashing():
    password = "securepassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# tests/test_ai_generation.py
@pytest.mark.asyncio
async def test_generate_caption(mock_openai):
    generator = TextGenerator()
    result = await generator.generate_caption(
        prompt="New summer collection",
        platform="instagram",
        tone="casual"
    )
    assert "caption" in result
    assert "hashtags" in result
    assert len(result["hashtags"]) > 0
```

**Integration Tests :**
```python
# tests/integration/test_post_flow.py
@pytest.mark.asyncio
async def test_full_post_creation_flow(client, auth_headers):
    # 1. Generate AI content
    gen_response = await client.post(
        "/api/v1/ai/generate-caption",
        json={"prompt": "Test product", "platform": "instagram"},
        headers=auth_headers
    )
    assert gen_response.status_code == 200
    content = gen_response.json()

    # 2. Create draft post
    post_response = await client.post(
        "/api/v1/content/posts",
        json={
            "caption": content["caption"],
            "platform": "instagram",
            "ai_generated": True
        },
        headers=auth_headers
    )
    assert post_response.status_code == 200
    post = post_response.json()

    # 3. Schedule post
    schedule_response = await client.post(
        f"/api/v1/content/posts/{post['id']}/schedule",
        json={"scheduled_at": "2025-06-15T18:00:00Z"},
        headers=auth_headers
    )
    assert schedule_response.status_code == 200
```

### Frontend Tests

**Component Tests (Jest + React Testing Library) :**
```tsx
// __tests__/components/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from '@/components/auth/LoginForm';

describe('LoginForm', () => {
  it('renders login form', () => {
    render(<LoginForm />);
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
  });

  it('shows error on invalid credentials', async () => {
    render(<LoginForm />);

    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'wrongpassword' }
    });
    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });
});
```

**E2E Tests (Playwright) :**
```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test('user can signup and login', async ({ page }) => {
  // Signup
  await page.goto('/register');
  await page.fill('input[name="email"]', 'newuser@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.fill('input[name="full_name"]', 'New User');
  await page.click('button[type="submit"]');

  // Should redirect to dashboard
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');

  // Logout
  await page.click('[aria-label="Profile menu"]');
  await page.click('text=Logout');

  // Login again
  await page.goto('/login');
  await page.fill('input[name="email"]', 'newuser@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
});
```

---

## 7. Deployment Plan

### Pre-Production Checklist

**Backend :**
- [ ] All environment variables configured
- [ ] Database migrations applied
- [ ] Secrets stored in AWS Secrets Manager
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Logging setup (structured JSON logs)
- [ ] Monitoring (Sentry error tracking)
- [ ] Health check endpoint (`/health`)

**Frontend :**
- [ ] Environment variables (NEXT_PUBLIC_API_URL, etc.)
- [ ] SEO meta tags
- [ ] Analytics (Google Analytics, Plausible)
- [ ] Error boundaries
- [ ] Loading states for all async operations
- [ ] Build optimization (bundle size < 500KB)

**Infrastructure :**
- [ ] SSL certificate configured
- [ ] Domain DNS pointing to CloudFront
- [ ] WAF rules (DDoS protection)
- [ ] Backup strategy (DB snapshots daily)
- [ ] Monitoring dashboards (CloudWatch, Datadog)

### Deployment Steps

**1. Database Setup :**
```bash
# Run migrations on production DB
alembic upgrade head

# Verify schema
psql $DATABASE_URL -c "\dt"
```

**2. Backend Deployment :**
```bash
# Build Docker image
docker build -t pyralys-api:v1.0.0 .

# Push to ECR
docker tag pyralys-api:v1.0.0 $ECR_REGISTRY/pyralys-api:v1.0.0
docker push $ECR_REGISTRY/pyralys-api:v1.0.0

# Update ECS service
aws ecs update-service \
  --cluster pyralys-prod \
  --service api \
  --force-new-deployment
```

**3. Frontend Deployment :**
```bash
# Build Next.js
npm run build

# Deploy to S3 + CloudFront
aws s3 sync out/ s3://pyralys-frontend-prod/
aws cloudfront create-invalidation \
  --distribution-id $CLOUDFRONT_ID \
  --paths "/*"
```

**4. Smoke Tests :**
```bash
# Health check
curl https://api.pyralys.com/health

# Test auth flow
curl -X POST https://api.pyralys.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@pyralys.com","password":"testpass"}'
```

**5. Monitoring :**
- [ ] Check Sentry for errors
- [ ] Verify logs in CloudWatch
- [ ] Monitor performance metrics (response times)
- [ ] Set up alerts (error rate > 1%, CPU > 80%)

---

## ⏱️ Timeline Recap

| Sprint | Dates | Focus | Team |
|--------|-------|-------|------|
| **Sprint 0** | Sem 1 | Infrastructure | 2 BE + 2 FE + 0.5 DevOps |
| **Sprint 1** | Sem 2 | Auth & Users | 1 BE + 1 FE |
| **Sprint 2** | Sem 3 | Instagram OAuth | 1 BE + 1 FE |
| **Sprint 3** | Sem 4 | AI Generation | 1 BE + 1 FE |
| **Sprint 4** | Sem 5 | Content Management | 2 BE + 1 FE |
| **Sprint 5** | Sem 6 | Scheduling & Publishing | 2 BE + 1 FE |
| **Sprint 6** | Sem 7 | Analytics | 1 BE + 2 FE |
| **Sprint 7** | Sem 8 | Billing | 1 BE + 1 FE |
| **Sprint 8** | Sem 9 | Polish & Deploy | 2 BE + 2 FE + 1 DevOps |

**Total Duration :** 9 semaines (2 mois)
**Total Effort :** ~60 dev-weeks

---

**Dernière mise à jour :** 31 Décembre 2025
**Auteur :** Équipe Développement Pyralys
**Version :** 1.0
