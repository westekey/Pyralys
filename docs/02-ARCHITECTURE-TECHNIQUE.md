# 🏗️ Architecture Technique - Pyralys

## Table des Matières
1. [Vue d'Ensemble Architecture](#1-vue-densemble-architecture)
2. [Stack Technologique Détaillée](#2-stack-technologique-détaillée)
3. [Architecture Backend](#3-architecture-backend)
4. [Architecture Frontend](#4-architecture-frontend)
5. [Infrastructure Cloud et DevOps](#5-infrastructure-cloud-et-devops)
6. [Sécurité et Compliance](#6-sécurité-et-compliance)
7. [Scalabilité et Performance](#7-scalabilité-et-performance)
8. [Intégrations Externes](#8-intégrations-externes)

---

## 1. Vue d'Ensemble Architecture

### Architecture Globale (Microservices)

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACES                            │
│  Web App (React/Next.js) │ Mobile App (React Native - Phase 2)      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          CDN (CloudFlare)                            │
│                    Static Assets + DDoS Protection                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Kong / AWS ALB)                    │
│   Rate Limiting │ Auth │ Load Balancing │ Request Routing           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  AUTH SERVICE    │    │  CORE API        │    │  WEBHOOK SERVICE │
│  (FastAPI)       │    │  (FastAPI)       │    │  (FastAPI)       │
│                  │    │                  │    │                  │
│ • JWT Auth       │    │ • REST API       │    │ • Instagram      │
│ • OAuth2         │    │ • GraphQL        │    │ • TikTok         │
│ • User Mgmt      │    │ • WebSockets     │    │ • Facebook       │
└──────────────────┘    └──────────────────┘    └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ CONTENT SERVICE  │    │  AI ENGINE       │    │ PUBLISHER        │
│ (FastAPI)        │    │  (Python)        │    │ (Celery Workers) │
│                  │    │                  │    │                  │
│ • CRUD Posts     │    │ • GPT-4 Text     │    │ • Instagram API  │
│ • Media Storage  │    │ • DALL-E Images  │    │ • TikTok API     │
│ • Templates      │    │ • Video Gen      │    │ • Facebook API   │
│ • Scheduling     │    │ • ML Predictions │    │ • Queue Mgmt     │
└──────────────────┘    └──────────────────┘    └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ ANALYTICS        │    │  NOTIFICATION    │    │  BILLING         │
│ SERVICE          │    │  SERVICE         │    │  SERVICE         │
│ (Python)         │    │  (Node.js)       │    │  (FastAPI)       │
│                  │    │                  │    │                  │
│ • Metrics        │    │ • Email (SendGrid│    │ • Stripe API     │
│ • Reports        │    │ • Push Notifs    │    │ • Subscriptions  │
│ • Predictions    │    │ • Webhooks       │    │ • Invoicing      │
└──────────────────┘    └──────────────────┘    └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                  │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ PostgreSQL   │  │  Redis       │  │  S3 / Blob   │             │
│  │ (Primary DB) │  │  (Cache +    │  │  (Media      │             │
│  │              │  │   Queue)     │  │   Storage)   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ TimescaleDB  │  │  Pinecone    │  │  Elasticsearch             │
│  │ (Time Series │  │  (Vector DB) │  │  (Search)    │             │
│  │  Analytics)  │  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MONITORING & OBSERVABILITY                        │
│  Datadog / New Relic │ Sentry │ LogDNA │ Prometheus + Grafana       │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux de Données Principaux

#### Flux 1 : Création de Contenu AI
```
User Request → Core API → AI Engine Service
                              │
                              ├──→ OpenAI GPT-4 (text generation)
                              ├──→ DALL-E 3 / Stability AI (image)
                              └──→ Runway ML / Pika (video - Phase 2)
                              │
                              ▼
                         Generated Content
                              │
                              ▼
                    Content Service (save draft)
                              │
                              ▼
                     User Preview & Edit
                              │
                              ▼
                    Approve & Schedule
                              │
                              ▼
                    Celery Queue → Publisher Service
                              │
                              ▼
                    Social Platform APIs
```

#### Flux 2 : Analytics Collection
```
Social Platform Webhook → Webhook Service
                              │
                              ▼
                        Validate & Parse
                              │
                              ▼
                    Analytics Service (process)
                              │
                              ▼
                    TimescaleDB (store metrics)
                              │
                              ▼
                    ML Model (predict performance)
                              │
                              ▼
                    Frontend Dashboard (real-time update via WebSocket)
```

---

## 2. Stack Technologique Détaillée

### Backend

#### Framework Principal : **FastAPI (Python 3.11+)**
**Pourquoi FastAPI ?**
- ✅ Performance excellente (comparable à Node.js)
- ✅ Async/await natif pour I/O non-bloquant
- ✅ Documentation auto-générée (OpenAPI/Swagger)
- ✅ Typage fort avec Pydantic
- ✅ Écosystème ML/AI riche (TensorFlow, PyTorch, etc.)

**Alternatives considérées :**
- ❌ Django REST Framework : trop lourd, moins performant
- ❌ Node.js/Express : moins bon pour AI/ML
- ⚠️ Go/Gin : excellente performance mais écosystème AI limité

**Structure FastAPI :**
```python
# app/main.py
from fastapi import FastAPI
from app.api.v1 import auth, content, analytics
from app.core.config import settings

app = FastAPI(
    title="Pyralys API",
    version="1.0.0",
    docs_url="/api/docs"
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
```

#### ORM : **SQLAlchemy 2.0 + Alembic**
- Migrations gérées automatiquement
- Support async avec asyncpg
- Relations complexes gérées élégamment

#### Task Queue : **Celery + Redis**
**Use cases :**
- Publication programmée de contenu
- Génération AI asynchrone (peut prendre 10-30s)
- Récupération analytics des plateformes (batch jobs)
- Envoi emails/notifications

**Configuration :**
```python
# celery_config.py
from celery import Celery

celery_app = Celery(
    "pyralys",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery_app.conf.task_routes = {
    "tasks.publish_content": {"queue": "publishing"},
    "tasks.generate_ai_content": {"queue": "ai_generation"},
    "tasks.fetch_analytics": {"queue": "analytics"}
}

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-analytics-every-hour": {
        "task": "tasks.fetch_analytics",
        "schedule": 3600.0,  # every hour
    }
}
```

#### Cache : **Redis**
**Stratégies de cache :**
- Session storage (TTL : 24h)
- API responses fréquentes (TTL : 5-15min)
- Rate limiting counters
- Celery broker et result backend

---

### Frontend

#### Framework : **Next.js 14+ (React 18)**
**Pourquoi Next.js ?**
- ✅ SSR pour SEO optimal
- ✅ API routes pour BFF (Backend-for-Frontend)
- ✅ Image optimization automatique
- ✅ File-based routing intuitif
- ✅ Edge functions pour performance

**Structure projet :**
```
frontend/
├── app/                    # Next.js 14 App Router
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/
│   │   ├── page.tsx       # Dashboard home
│   │   ├── content/       # Content studio
│   │   ├── analytics/     # Analytics
│   │   └── settings/
│   ├── layout.tsx
│   └── page.tsx           # Landing page
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── dashboard/
│   ├── content-studio/
│   └── analytics/
├── lib/
│   ├── api.ts             # API client (axios/fetch)
│   ├── auth.ts            # Auth utilities
│   └── utils.ts
├── hooks/
│   ├── useAuth.ts
│   ├── useContent.ts
│   └── useAnalytics.ts
├── store/                 # State management
│   └── zustand/           # Zustand stores
└── styles/
    └── globals.css        # Tailwind CSS
```

#### UI Library : **shadcn/ui + Tailwind CSS**
**Composants clés :**
- Button, Input, Select (formulaires)
- Dialog, Sheet (modales)
- Card, Table (affichage données)
- Calendar, DatePicker (scheduling)
- Chart (Recharts pour analytics)

#### State Management : **Zustand**
**Pourquoi pas Redux ?**
- ✅ Zustand = plus simple, moins de boilerplate
- ✅ Performance excellente
- ✅ DevTools support

**Example store :**
```typescript
// store/contentStore.ts
import create from 'zustand';

interface ContentStore {
  drafts: Post[];
  scheduled: Post[];
  published: Post[];
  addDraft: (post: Post) => void;
  publishPost: (id: string) => Promise<void>;
}

export const useContentStore = create<ContentStore>((set, get) => ({
  drafts: [],
  scheduled: [],
  published: [],

  addDraft: (post) => set((state) => ({
    drafts: [...state.drafts, post]
  })),

  publishPost: async (id) => {
    const response = await api.publishPost(id);
    // Update state
  }
}));
```

#### Forms : **React Hook Form + Zod**
- Validation schema avec Zod
- Performance optimale (minimal re-renders)

---

### AI & Machine Learning

#### LLM pour Génération Texte

**Option 1 : OpenAI GPT-4** (Recommandé MVP)
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_caption(
    product_description: str,
    platform: str,
    tone: str = "casual"
) -> str:
    system_prompt = f"""Tu es un expert en copywriting pour {platform}.
    Génère une caption engageante en style {tone}."""

    response = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": product_description}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content
```

**Pricing :**
- GPT-4 Turbo : $0.01/1K tokens (input), $0.03/1K tokens (output)
- Estimation : 200 tokens/caption → ~$0.006/caption
- Pour 10,000 captions/mois : ~$60/mois

**Option 2 : Anthropic Claude 3** (Alternative)
- Meilleur pour instructions complexes
- Contexte window plus large (200K tokens)
- Pricing similaire

**Option 3 : Mistral AI / Llama 3** (Budget)
- Open-source, self-hosted possible
- Coût moindre mais qualité inférieure

#### Génération Images

**Option 1 : DALL-E 3** (Recommandé)
```python
async def generate_image(prompt: str, size: str = "1024x1024") -> str:
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    # Download and upload to S3
    return await upload_to_s3(image_url)
```

**Pricing :**
- DALL-E 3 Standard : $0.040 per image (1024×1024)
- DALL-E 3 HD : $0.080 per image

**Option 2 : Stability AI (Stable Diffusion XL)**
- $0.02 per image (moins cher)
- Qualité légèrement inférieure
- Meilleur contrôle créatif (LoRA, ControlNet)

**Option 3 : Midjourney API** (si disponible)
- Qualité supérieure
- Pas d'API officielle (utiliser service tiers comme GoAPI)

#### Génération Vidéo (Phase 2)

**Options explorées :**
- **Runway ML Gen-2** : $0.05/seconde vidéo
- **Pika Labs** : Access limited beta
- **OpenAI Sora** : Pas encore d'API publique (2025)

**Alternative MVP : Templates-based video**
- Utiliser FFmpeg + templates After Effects
- Assemblage automatique : clips + musique + transitions
- Moins "AI-generated" mais plus contrôlable

```python
import ffmpeg

async def create_video_from_template(
    images: List[str],
    music_url: str,
    template_id: str
) -> str:
    """Create video using FFmpeg and predefined templates"""
    # Implementation with FFmpeg
    pass
```

---

### Databases

#### PostgreSQL 15+ (Primary Database)
**Schema principal :**
```sql
-- Users & Auth
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    full_name VARCHAR(255),
    plan_type VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Social Accounts Connected
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'instagram', 'tiktok', etc.
    platform_user_id VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    account_username VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content Posts
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    caption TEXT,
    media_urls JSONB, -- Array of image/video URLs
    platform VARCHAR(50),
    status VARCHAR(50) DEFAULT 'draft', -- draft, scheduled, published, failed
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    ai_generated BOOLEAN DEFAULT false,
    generation_params JSONB, -- Store AI params used
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Post Performance Metrics
CREATE TABLE post_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    platform_post_id VARCHAR(255),
    impressions INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2),
    fetched_at TIMESTAMP DEFAULT NOW()
);

-- Brand Voice Learning
CREATE TABLE brand_voice (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tone VARCHAR(100), -- casual, professional, funny, etc.
    keywords JSONB, -- Array of brand keywords
    avoid_words JSONB,
    sample_captions TEXT[], -- Past approved captions for learning
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Content Templates
CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    category VARCHAR(100),
    platform VARCHAR(50),
    template_data JSONB, -- Structured template config
    preview_url VARCHAR(500),
    is_premium BOOLEAN DEFAULT false,
    price_cents INTEGER DEFAULT 0,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes pour performance :**
```sql
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
CREATE INDEX idx_posts_scheduled ON posts(scheduled_at) WHERE status = 'scheduled';
CREATE INDEX idx_social_accounts_user ON social_accounts(user_id);
CREATE INDEX idx_post_metrics_post ON post_metrics(post_id);
```

#### TimescaleDB (Analytics Time-Series)
Extension PostgreSQL optimisée pour time-series data.

```sql
-- Hypertable pour métriques temporelles
CREATE TABLE analytics_timeseries (
    time TIMESTAMPTZ NOT NULL,
    user_id UUID NOT NULL,
    post_id UUID,
    metric_name VARCHAR(100),
    metric_value NUMERIC,
    platform VARCHAR(50)
);

SELECT create_hypertable('analytics_timeseries', 'time');

-- Compression automatique des vieilles données
ALTER TABLE analytics_timeseries SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'user_id, platform'
);

SELECT add_compression_policy('analytics_timeseries', INTERVAL '7 days');
```

#### Redis (Cache & Queue)
**Use cases :**
```python
# Session cache
redis_client.setex(f"session:{session_id}", 86400, user_data)

# Rate limiting
key = f"rate_limit:{user_id}:{endpoint}"
count = redis_client.incr(key)
if count == 1:
    redis_client.expire(key, 3600)  # 1 hour window
if count > 100:
    raise RateLimitExceeded()

# Cache API responses
cache_key = f"analytics:{user_id}:{date_range}"
cached = redis_client.get(cache_key)
if cached:
    return json.loads(cached)
# Else fetch from DB and cache
redis_client.setex(cache_key, 900, json.dumps(data))  # 15 min TTL
```

#### Pinecone (Vector Database)
Pour recherche sémantique et recommendations.

**Use case :** Trouver templates similaires à un contenu donné
```python
import pinecone
from openai import OpenAI

# Initialize
pinecone.init(api_key=settings.PINECONE_API_KEY)
index = pinecone.Index("content-templates")

# Embed user query
client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Je veux un post Instagram pour promouvoir un nouveau parfum"
)
query_embedding = response.data[0].embedding

# Search similar templates
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True
)

# Results contient templates similaires sémantiquement
```

---

## 3. Architecture Backend

### Microservices Détaillés

#### Service 1 : Auth Service
**Responsabilités :**
- Authentification utilisateurs (email/password, OAuth)
- Gestion JWT tokens
- Password reset, email verification
- Session management

**Endpoints clés :**
```
POST   /auth/register
POST   /auth/login
POST   /auth/refresh
POST   /auth/logout
POST   /auth/forgot-password
POST   /auth/reset-password
GET    /auth/verify-email/:token
POST   /auth/oauth/google
POST   /auth/oauth/facebook
```

**Technologies :**
- FastAPI
- Passlib (password hashing)
- Python-JOSE (JWT)
- OAuth libraries (authlib)

#### Service 2 : Content Service
**Responsabilités :**
- CRUD operations sur posts
- File uploads (images, vidéos)
- Template management
- Scheduling logic

**Endpoints clés :**
```
GET    /content/posts
POST   /content/posts
GET    /content/posts/:id
PUT    /content/posts/:id
DELETE /content/posts/:id
POST   /content/posts/:id/schedule
POST   /content/posts/:id/publish-now
GET    /content/templates
POST   /content/upload-media
```

#### Service 3 : AI Engine Service
**Responsabilités :**
- Génération texte (captions, hashtags)
- Génération images
- Performance predictions
- Content optimization suggestions

**Endpoints clés :**
```
POST   /ai/generate-caption
POST   /ai/generate-image
POST   /ai/generate-hashtags
POST   /ai/predict-performance
POST   /ai/optimize-content
POST   /ai/suggest-topics
```

**Architecture interne :**
```python
# ai_engine/services/text_generator.py
class TextGenerator:
    def __init__(self):
        self.openai_client = AsyncOpenAI()
        self.cache = Redis()

    async def generate_caption(
        self,
        context: ContentContext,
        user_preferences: UserPreferences
    ) -> GeneratedContent:
        # Check cache first
        cache_key = self._build_cache_key(context)
        if cached := await self.cache.get(cache_key):
            return json.loads(cached)

        # Generate with LLM
        prompt = self._build_prompt(context, user_preferences)
        result = await self._call_llm(prompt)

        # Cache for 1 hour
        await self.cache.setex(cache_key, 3600, json.dumps(result))

        return result
```

#### Service 4 : Publisher Service (Celery Workers)
**Responsabilités :**
- Publication automatique sur plateformes sociales
- Retry logic en cas d'échec
- Status tracking
- Webhooks handling

**Tasks Celery :**
```python
# publisher/tasks.py
from celery import Task

@celery_app.task(bind=True, max_retries=3)
def publish_to_instagram(self, post_id: str):
    try:
        post = get_post_from_db(post_id)
        account = get_social_account(post.user_id, "instagram")

        # Publish via Instagram API
        result = instagram_api.publish_post(
            access_token=account.access_token,
            caption=post.caption,
            image_url=post.media_urls[0]
        )

        # Update post status
        update_post_status(post_id, "published", platform_post_id=result.id)

        # Send notification to user
        send_notification(post.user_id, f"Post published successfully!")

    except Exception as exc:
        # Retry with exponential backoff
        self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

#### Service 5 : Analytics Service
**Responsabilités :**
- Fetch metrics from social platforms
- Calculate derived metrics (engagement rate, etc.)
- Store time-series data
- Generate reports

**Jobs périodiques :**
```python
@celery_app.task
def fetch_instagram_insights():
    """Run every hour to fetch latest metrics"""
    active_accounts = get_active_instagram_accounts()

    for account in active_accounts:
        recent_posts = get_recent_posts(account.user_id, days=7)

        for post in recent_posts:
            metrics = instagram_api.get_post_insights(
                post_id=post.platform_post_id,
                access_token=account.access_token
            )

            save_metrics_to_timescale(post.id, metrics)
```

---

## 4. Architecture Frontend

### Pages Principales

#### 1. Landing Page (Public)
**Composants :**
- Hero section avec CTA
- Features showcase
- Pricing table
- Testimonials (fake initialement, puis réels)
- FAQ
- Footer avec liens

#### 2. Dashboard (Protected)
**Composants :**
```tsx
// app/(dashboard)/page.tsx
import { StatsOverview } from '@/components/dashboard/StatsOverview';
import { RecentPosts } from '@/components/dashboard/RecentPosts';
import { PerformanceChart } from '@/components/dashboard/PerformanceChart';
import { QuickActions } from '@/components/dashboard/QuickActions';

export default function DashboardPage() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      {/* Stats Cards */}
      <StatsOverview />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {/* Performance Chart */}
        <PerformanceChart />

        {/* Quick Actions */}
        <QuickActions />
      </div>

      {/* Recent Posts Table */}
      <RecentPosts />
    </div>
  );
}
```

**Métriques affichées :**
- Total posts published (last 30 days)
- Average engagement rate
- Total reach
- Followers growth

#### 3. Content Studio
**Features :**
- AI generation panel
- Media upload
- Preview multi-plateformes
- Scheduling calendar
- Draft management

```tsx
// components/content-studio/AIGenerationPanel.tsx
export function AIGenerationPanel() {
  const [prompt, setPrompt] = useState('');
  const [generatedContent, setGeneratedContent] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const response = await api.post('/ai/generate-caption', {
        prompt,
        platform: 'instagram',
        tone: 'casual'
      });
      setGeneratedContent(response.data);
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
      <CardContent>
        <Textarea
          placeholder="Describe your product or topic..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <Button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="mt-4"
        >
          {isGenerating ? 'Generating...' : 'Generate Caption'}
        </Button>

        {generatedContent && (
          <div className="mt-6 p-4 bg-gray-50 rounded">
            <h4 className="font-semibold mb-2">Generated Caption:</h4>
            <p>{generatedContent.caption}</p>

            <h4 className="font-semibold mt-4 mb-2">Hashtags:</h4>
            <div className="flex flex-wrap gap-2">
              {generatedContent.hashtags.map(tag => (
                <span key={tag} className="text-blue-600">#{tag}</span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

#### 4. Analytics Dashboard
**Composants :**
- Date range selector
- Performance charts (Line, Bar, Pie)
- Posts comparison table
- Export to PDF/CSV

**Charts avec Recharts :**
```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

export function EngagementChart({ data }) {
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="engagement_rate" stroke="#8884d8" />
      <Line type="monotone" dataKey="reach" stroke="#82ca9d" />
    </LineChart>
  );
}
```

---

## 5. Infrastructure Cloud et DevOps

### Cloud Provider : **AWS** (Recommandé)

**Alternatives :**
- Google Cloud Platform (GCP)
- Microsoft Azure
- DigitalOcean (moins cher mais moins de services)

### Architecture AWS

```
┌─────────────────────────────────────────────────────────────┐
│                      Route 53 (DNS)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              CloudFront (CDN) + WAF                         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│  S3 (Static      │                  │  ALB (Load       │
│  Frontend)       │                  │  Balancer)       │
└──────────────────┘                  └──────────────────┘
                                                │
                    ┌───────────────────────────┼───────────────┐
                    ▼                           ▼               ▼
              ┌──────────┐              ┌──────────┐     ┌──────────┐
              │  ECS     │              │  ECS     │     │  Lambda  │
              │  (API)   │              │  (Workers)     │  (Webhooks)
              └──────────┘              └──────────┘     └──────────┘
                    │                           │               │
                    └───────────────────────────┼───────────────┘
                                                ▼
                    ┌───────────────────────────────────────────┐
                    │           RDS PostgreSQL                  │
                    │           ElastiCache Redis               │
                    │           S3 (Media Storage)              │
                    └───────────────────────────────────────────┘
```

**Services AWS utilisés :**

| Service | Usage | Coût estimé/mois |
|---------|-------|------------------|
| **ECS Fargate** | Backend APIs (4 containers) | $150 |
| **RDS PostgreSQL** | db.t3.medium | $100 |
| **ElastiCache Redis** | cache.t3.micro | $20 |
| **S3** | Media storage (500GB) | $12 |
| **CloudFront** | CDN (1TB transfer) | $85 |
| **Lambda** | Webhooks processing | $10 |
| **ALB** | Load balancing | $25 |
| **Route 53** | DNS | $1 |
| **CloudWatch** | Monitoring & Logs | $30 |
| **SES** | Email sending | $10 |
| **Secrets Manager** | API keys storage | $5 |
| **TOTAL** | | **~$450/mois** |

### CI/CD Pipeline

**GitHub Actions Workflow :**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=app tests/

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-1

      - name: Login to ECR
        run: aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}

      - name: Build and push Docker image
        run: |
          docker build -t pyralys-api:latest .
          docker tag pyralys-api:latest ${{ secrets.ECR_REGISTRY }}/pyralys-api:latest
          docker push ${{ secrets.ECR_REGISTRY }}/pyralys-api:latest

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster pyralys-prod --service api --force-new-deployment
```

### Infrastructure as Code (Terraform)

**Exemple configuration ECS :**
```hcl
# terraform/ecs.tf
resource "aws_ecs_cluster" "pyralys" {
  name = "pyralys-${var.environment}"
}

resource "aws_ecs_task_definition" "api" {
  family                   = "pyralys-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([{
    name  = "api"
    image = "${var.ecr_registry}/pyralys-api:latest"
    portMappings = [{
      containerPort = 8000
      protocol      = "tcp"
    }]
    environment = [
      {
        name  = "DATABASE_URL"
        value = var.database_url
      },
      {
        name  = "REDIS_URL"
        value = var.redis_url
      }
    ]
    secrets = [
      {
        name      = "OPENAI_API_KEY"
        valueFrom = aws_secretsmanager_secret.openai_key.arn
      }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/pyralys-api"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "api" {
  name            = "api"
  cluster         = aws_ecs_cluster.pyralys.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 2  # 2 instances pour HA

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8000
  }
}
```

---

## 6. Sécurité et Compliance

### Authentication & Authorization

**JWT Token Strategy :**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**OAuth 2.0 pour connexion sociale :**
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    # Create or login user
```

### Rate Limiting

**Implementation avec SlowAPI :**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/ai/generate-caption")
@limiter.limit("10/minute")  # Max 10 générations/minute
async def generate_caption(request: Request):
    pass
```

### Data Encryption

**At rest :**
- RDS encryption enabled (AES-256)
- S3 bucket encryption (SSE-S3)
- Secrets Manager pour API keys

**In transit :**
- HTTPS only (TLS 1.3)
- Certificate management via AWS Certificate Manager

### GDPR Compliance

**Fonctionnalités requises :**
```python
# Data export
@app.get("/api/v1/user/export-data")
async def export_user_data(current_user: User):
    """Export all user data in JSON format (GDPR right to data portability)"""
    data = {
        "user": current_user.dict(),
        "posts": await get_all_user_posts(current_user.id),
        "analytics": await get_all_user_analytics(current_user.id),
        "connected_accounts": await get_user_social_accounts(current_user.id)
    }
    return JSONResponse(content=data)

# Data deletion
@app.delete("/api/v1/user/delete-account")
async def delete_account(current_user: User, password: str):
    """Permanently delete user account and all associated data"""
    # Verify password
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Delete from all tables (CASCADE will handle most)
    await delete_user_completely(current_user.id)

    # Delete media files from S3
    await delete_user_media(current_user.id)

    return {"message": "Account deleted successfully"}
```

---

## 7. Scalabilité et Performance

### Horizontal Scaling

**Auto-scaling ECS :**
```hcl
resource "aws_appautoscaling_target" "api" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.pyralys.name}/${aws_ecs_service.api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "api_cpu" {
  name               = "api-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.api.resource_id
  scalable_dimension = aws_appautoscaling_target.api.scalable_dimension
  service_namespace  = aws_appautoscaling_target.api.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value = 70.0  # Scale when CPU > 70%

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}
```

### Caching Strategy

**Multi-layer caching :**
```python
from functools import lru_cache
from app.core.redis import redis_client

# Layer 1: In-memory cache (LRU)
@lru_cache(maxsize=1000)
def get_user_plan(user_id: str) -> str:
    """Cached in memory for ultra-fast access"""
    return fetch_from_db(user_id).plan

# Layer 2: Redis cache
async def get_user_analytics(user_id: str, date_range: str):
    cache_key = f"analytics:{user_id}:{date_range}"

    # Try cache first
    if cached := await redis_client.get(cache_key):
        return json.loads(cached)

    # Fetch from DB (expensive query)
    data = await fetch_analytics_from_db(user_id, date_range)

    # Cache for 15 minutes
    await redis_client.setex(cache_key, 900, json.dumps(data))

    return data
```

### Database Optimization

**Read Replicas :**
```python
from sqlalchemy import create_engine

# Master (write)
engine_master = create_engine(settings.DATABASE_WRITE_URL)

# Replica (read)
engine_replica = create_engine(settings.DATABASE_READ_URL)

class DatabaseRouter:
    def get_engine(self, operation: str):
        if operation in ['SELECT', 'GET']:
            return engine_replica
        return engine_master
```

**Connection Pooling :**
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,  # Max 20 connections
    max_overflow=10,  # Allow 10 extra in high load
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600  # Recycle connections every hour
)
```

---

## 8. Intégrations Externes

### Meta (Instagram + Facebook)

**OAuth Flow :**
```python
FACEBOOK_SCOPES = [
    "instagram_basic",
    "instagram_content_publish",
    "instagram_manage_comments",
    "instagram_manage_insights",
    "pages_show_list",
    "pages_read_engagement"
]

@app.get("/api/v1/social/instagram/connect")
async def connect_instagram(current_user: User):
    redirect_uri = f"{settings.FRONTEND_URL}/oauth/instagram/callback"

    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={settings.FACEBOOK_APP_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={','.join(FACEBOOK_SCOPES)}&"
        f"state={current_user.id}"
    )

    return {"auth_url": auth_url}

@app.get("/api/v1/social/instagram/callback")
async def instagram_callback(code: str, state: str):
    # Exchange code for access token
    response = requests.post(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "redirect_uri": f"{settings.FRONTEND_URL}/oauth/instagram/callback",
            "code": code
        }
    )

    access_token = response.json()["access_token"]

    # Get long-lived token
    long_lived_token = exchange_for_long_lived_token(access_token)

    # Get user's Instagram accounts
    ig_accounts = get_instagram_accounts(long_lived_token)

    # Save to database
    await save_social_account(
        user_id=state,
        platform="instagram",
        access_token=long_lived_token,
        accounts=ig_accounts
    )
```

**Publishing Content :**
```python
async def publish_to_instagram(
    ig_user_id: str,
    access_token: str,
    image_url: str,
    caption: str
) -> dict:
    """Publish image post to Instagram"""

    # Step 1: Create media container
    create_response = requests.post(
        f"https://graph.facebook.com/v18.0/{ig_user_id}/media",
        params={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token
        }
    )

    container_id = create_response.json()["id"]

    # Step 2: Publish container
    publish_response = requests.post(
        f"https://graph.facebook.com/v18.0/{ig_user_id}/media_publish",
        params={
            "creation_id": container_id,
            "access_token": access_token
        }
    )

    return publish_response.json()
```

### TikTok

**Note :** TikTok Content Posting API nécessite application pour accès.

```python
# TikTok OAuth (simplifié)
@app.get("/api/v1/social/tiktok/connect")
async def connect_tiktok(current_user: User):
    auth_url = (
        f"https://www.tiktok.com/v2/auth/authorize/?"
        f"client_key={settings.TIKTOK_CLIENT_KEY}&"
        f"scope=user.info.basic,video.upload,video.publish&"
        f"response_type=code&"
        f"redirect_uri={settings.TIKTOK_REDIRECT_URI}&"
        f"state={current_user.id}"
    )
    return {"auth_url": auth_url}

# Video upload
async def upload_to_tiktok(
    access_token: str,
    video_url: str,
    title: str,
    privacy_level: str = "PUBLIC_TO_EVERYONE"
) -> dict:
    """Upload video to TikTok"""

    # Initialize upload
    init_response = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "post_info": {
                "title": title,
                "privacy_level": privacy_level,
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": await get_video_size(video_url),
                "chunk_size": 5000000,  # 5MB chunks
                "total_chunk_count": await calculate_chunks(video_url)
            }
        }
    )

    publish_id = init_response.json()["data"]["publish_id"]
    upload_url = init_response.json()["data"]["upload_url"]

    # Upload video chunks
    await upload_video_chunks(video_url, upload_url)

    return {"publish_id": publish_id}
```

### OpenAI

**Gestion des erreurs et retry :**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_with_gpt4(prompt: str, max_tokens: int = 500) -> str:
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a social media expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )

        return response.choices[0].message.content

    except openai.RateLimitError:
        logger.warning("OpenAI rate limit hit, retrying...")
        raise
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise
```

### Stripe (Payments)

```python
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@app.post("/api/v1/billing/create-checkout-session")
async def create_checkout_session(plan: str, current_user: User):
    """Create Stripe checkout session for subscription"""

    price_id = {
        "pro": "price_pro_monthly_xxxxx",
        "business": "price_business_monthly_xxxxx"
    }[plan]

    session = stripe.checkout.Session.create(
        customer_email=current_user.email,
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1
        }],
        mode="subscription",
        success_url=f"{settings.FRONTEND_URL}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.FRONTEND_URL}/billing/cancel",
        metadata={
            "user_id": str(current_user.id)
        }
    )

    return {"checkout_url": session.url}

@app.post("/api/v1/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]

        # Upgrade user plan
        await upgrade_user_plan(user_id, session["subscription"])

    elif event["type"] == "customer.subscription.deleted":
        subscription_id = event["data"]["object"]["id"]

        # Downgrade to free plan
        await downgrade_user_plan(subscription_id)

    return {"status": "success"}
```

---

## 📋 Résumé des Décisions Techniques

| Composant | Technologie Choisie | Alternative | Justification |
|-----------|---------------------|-------------|---------------|
| **Backend Framework** | FastAPI | Django, Express.js | Performance + async + AI ecosystem |
| **Frontend** | Next.js 14 | Remix, Vite+React | SSR, SEO, DX optimal |
| **Database** | PostgreSQL | MySQL, MongoDB | Robustesse, relations complexes, JSON support |
| **Cache** | Redis | Memcached | Polyvalence (cache + queue + pub/sub) |
| **Queue** | Celery | BullMQ, RabbitMQ | Mature, Python-native |
| **Cloud** | AWS | GCP, Azure | Ecosystem complet, pricing |
| **Container Orchestration** | ECS Fargate | Kubernetes, Docker Swarm | Managed, moins de complexité |
| **CDN** | CloudFront | Cloudflare | Intégration AWS native |
| **Monitoring** | Datadog | New Relic, Grafana | APM + logs + metrics unified |
| **Error Tracking** | Sentry | Rollbar, Bugsnag | Best-in-class, DX |
| **LLM** | OpenAI GPT-4 | Claude 3, Llama 3 | Qualité et documentation |
| **Image Gen** | DALL-E 3 | Stable Diffusion, Midjourney | Facilité intégration |

---

## ⏰ Temps Estimés de Développement

| Phase | Durée | Effort (dev-weeks) |
|-------|-------|-------------------|
| **Setup infrastructure** | 1 semaine | 1 dev × 1 sem = 1 |
| **Auth service** | 1 semaine | 1 dev × 1 sem = 1 |
| **Content service** | 2 semaines | 2 devs × 2 sem = 4 |
| **AI Engine service** | 2 semaines | 1 dev × 2 sem = 2 |
| **Publisher service** | 2 semaines | 1 dev × 2 sem = 2 |
| **Analytics service** | 1 semaine | 1 dev × 1 sem = 1 |
| **Frontend (all pages)** | 4 semaines | 2 devs × 4 sem = 8 |
| **Integration tests** | 1 semaine | 2 devs × 1 sem = 2 |
| **TOTAL MVP** | **8 semaines** | **21 dev-weeks** |

**Équipe recommandée :**
- 2 Backend developers (Python/FastAPI)
- 2 Frontend developers (React/Next.js)
- 0.5 DevOps engineer (part-time)

---

## 🚨 Risques Techniques Potentiels

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| **API Instagram limitations** | Élevé | Moyenne | Fallback manuel, quotas utilisateurs clairs |
| **OpenAI costs explosion** | Élevé | Faible | Rate limiting strict, caching agressif |
| **Scalability issues** | Moyen | Moyenne | Architecture microservices, auto-scaling |
| **Data privacy breach** | Critique | Faible | Security audit, encryption, GDPR compliance |
| **TikTok API access refusé** | Moyen | Moyenne | Démarrer sans TikTok, ajouter en Phase 2 |
| **Performance dégradation** | Moyen | Moyenne | Load testing, monitoring proactif |

---

**Dernière mise à jour :** 31 Décembre 2025
**Auteur :** Équipe Technique Pyralys
**Version :** 1.0
