# 🎨 Conception UX/UI - Pyralys

## Table des Matières
1. [Principes de Design](#1-principes-de-design)
2. [Design System](#2-design-system)
3. [Wireframes et User Flows](#3-wireframes-et-user-flows)
4. [Maquettes Détaillées](#4-maquettes-détaillées)
5. [Responsive Design](#5-responsive-design)
6. [Onboarding Intelligent](#6-onboarding-intelligent)
7. [Interactions et Microinteractions](#7-interactions-et-microinteractions)
8. [Accessibilité](#8-accessibilité)

---

## 1. Principes de Design

### Vision UX de Pyralys

**"Empowering creators with AI, not replacing them"**

L'interface doit refléter cette philosophie :
- L'IA est un **assistant**, pas un automate
- L'utilisateur garde le **contrôle créatif final**
- La complexité technique est **masquée** mais accessible si nécessaire
- Chaque action a un **feedback clair et immédiat**

### Principes Directeurs

#### 1. Simplicité avant tout
- Interface épurée, pas d'encombrement visuel
- Maximum 3 niveaux de navigation
- Actions principales accessibles en <2 clics
- Hiérarchie visuelle claire

#### 2. Rapidité et Efficacité
- Temps de génération AI affiché en temps réel
- Shortcuts clavier pour power users
- Batch operations (sélectionner plusieurs posts)
- Auto-save systématique (pas de bouton "Save")

#### 3. Transparence
- Montrer à l'utilisateur ce que l'IA fait (loading states explicites)
- Afficher les coûts (tokens AI utilisés, quotas restants)
- Prédictions accompagnées de leur niveau de confiance

#### 4. Feedback Positif
- Célébrer les succès (animations de publication réussie)
- Transformer les erreurs en opportunités d'apprentissage
- Gamification subtile (streaks de publication, achievements)

#### 5. Personnalisation Progressive
- Interface simple par défaut
- Options avancées révélées progressivement
- Adaptation à l'usage (recommandations de plus en plus précises)

---

## 2. Design System

### Palette de Couleurs

#### Couleurs Primaires
```css
/* Brand Colors */
--primary-500: #6366F1;      /* Indigo - Action principale */
--primary-600: #4F46E5;      /* Hover state */
--primary-700: #4338CA;      /* Active state */
--primary-50:  #EEF2FF;      /* Backgrounds légers */

/* Accent */
--accent-500: #EC4899;       /* Pink - Accents créatifs */
--accent-600: #DB2777;

/* Success */
--success-500: #10B981;      /* Green - Succès, publication */
--success-600: #059669;

/* Warning */
--warning-500: #F59E0B;      /* Amber - Attention, quotas */
--warning-600: #D97706;

/* Error */
--error-500: #EF4444;        /* Red - Erreurs */
--error-600: #DC2626;
```

#### Couleurs Neutres (Grays)
```css
--gray-50:  #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-300: #D1D5DB;
--gray-400: #9CA3AF;
--gray-500: #6B7280;
--gray-600: #4B5563;
--gray-700: #374151;
--gray-800: #1F2937;
--gray-900: #111827;
```

#### Couleurs par Plateforme (Social Icons)
```css
--instagram: linear-gradient(45deg, #F58529, #DD2A7B, #8134AF, #515BD4);
--tiktok: #000000;
--facebook: #1877F2;
--linkedin: #0A66C2;
--youtube: #FF0000;
--twitter: #1DA1F2;
```

### Typographie

#### Fonts
```css
/* Display / Headings */
--font-display: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Body Text */
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Monospace (Code, metrics) */
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```

#### Échelle Typographique
```css
--text-xs:   0.75rem;   /* 12px - Labels, captions */
--text-sm:   0.875rem;  /* 14px - Body small */
--text-base: 1rem;      /* 16px - Body default */
--text-lg:   1.125rem;  /* 18px - Body large */
--text-xl:   1.25rem;   /* 20px - Subtitle */
--text-2xl:  1.5rem;    /* 24px - Heading 3 */
--text-3xl:  1.875rem;  /* 30px - Heading 2 */
--text-4xl:  2.25rem;   /* 36px - Heading 1 */
--text-5xl:  3rem;      /* 48px - Display */
```

### Spacing System (4px base)
```css
--spacing-1:  0.25rem;  /* 4px */
--spacing-2:  0.5rem;   /* 8px */
--spacing-3:  0.75rem;  /* 12px */
--spacing-4:  1rem;     /* 16px */
--spacing-5:  1.25rem;  /* 20px */
--spacing-6:  1.5rem;   /* 24px */
--spacing-8:  2rem;     /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
```

### Border Radius
```css
--radius-sm: 0.375rem;  /* 6px - Inputs, tags */
--radius-md: 0.5rem;    /* 8px - Cards, buttons */
--radius-lg: 0.75rem;   /* 12px - Modals */
--radius-xl: 1rem;      /* 16px - Featured elements */
--radius-full: 9999px;  /* Pills, avatars */
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
             0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
             0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
             0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

### Composants UI Réutilisables

#### Button
```tsx
// components/ui/Button.tsx
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled,
  loading
}: ButtonProps) {
  const baseStyles = 'font-medium rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    outline: 'border-2 border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-primary-500',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
    danger: 'bg-error-600 text-white hover:bg-error-700 focus:ring-error-500'
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button
      className={cn(baseStyles, variants[variant], sizes[size])}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <Spinner size="sm" />
          {children}
        </span>
      ) : children}
    </button>
  );
}
```

#### Card
```tsx
// components/ui/Card.tsx
export function Card({ children, className, ...props }) {
  return (
    <div
      className={cn(
        'bg-white rounded-lg shadow-md p-6 transition-shadow hover:shadow-lg',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children }) {
  return <div className="mb-4">{children}</div>;
}

export function CardTitle({ children }) {
  return <h3 className="text-xl font-semibold text-gray-900">{children}</h3>;
}

export function CardContent({ children }) {
  return <div className="text-gray-600">{children}</div>;
}
```

#### Badge
```tsx
// components/ui/Badge.tsx
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  const variants = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-success-100 text-success-800',
    warning: 'bg-warning-100 text-warning-800',
    error: 'bg-error-100 text-error-800',
    info: 'bg-primary-100 text-primary-800'
  };

  return (
    <span className={cn(
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
      variants[variant]
    )}>
      {children}
    </span>
  );
}
```

---

## 3. Wireframes et User Flows

### User Flow Principal : Création et Publication de Contenu

```
┌─────────────────────────────────────────────────────────┐
│                    [DASHBOARD]                          │
│  "Recent Posts" │ "Performance" │ "Quick Actions"       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              [Click "Create New Post"]
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              [CONTENT STUDIO - Empty State]             │
│                                                         │
│   Option 1: "Generate with AI" ───────────┐            │
│   Option 2: "Upload Your Own"             │            │
│   Option 3: "Use Template"                │            │
└───────────────────────────────────────────┼─────────────┘
                                            │
                                            ▼
                        [AI GENERATION MODAL]
                                            │
        ┌───────────────────────────────────┼───────────┐
        │                                   │           │
        ▼                                   ▼           ▼
  [Text Prompt]                    [Select Platform]  [Choose Tone]
  "Describe your                   ☑ Instagram        ○ Casual
   product/topic"                  ☐ TikTok           ○ Professional
                                   ☐ Facebook         ● Funny
                                                      ○ Inspirational
        │                                   │           │
        └───────────────┬───────────────────┴───────────┘
                        ▼
              [Click "Generate Content"]
                        │
                        ▼ (Loading 5-10s)
              ┌─────────────────┐
              │ 🤖 AI is        │
              │ generating your │
              │ content...      │
              └─────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│          [CONTENT PREVIEW & EDIT]                       │
│                                                         │
│  ┌─────────────────┐  ┌──────────────────────────────┐ │
│  │  Image Preview  │  │  Caption:                    │ │
│  │                 │  │  "Check out our new product  │ │
│  │  [Generated     │  │   Perfect for summer! 🌞"    │ │
│  │   Image]        │  │                              │ │
│  │                 │  │  Hashtags:                   │ │
│  │  [Regenerate]   │  │  #fashion #summer #style ... │ │
│  └─────────────────┘  │                              │ │
│                       │  [Edit Caption]              │ │
│                       │  [Regenerate Hashtags]       │ │
│                       └──────────────────────────────┘ │
│                                                         │
│  AI Prediction Score: ⭐⭐⭐⭐☆ 8.2/10                    │
│  "Great potential! Try posting at 6 PM for best reach" │
│                                                         │
│  [← Back]  [Save as Draft]  [Schedule] [Publish Now →] │
└─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   [Save Draft]   [Schedule]     [Publish Now]
        │               │               │
        │               ▼               │
        │      ┌─────────────────┐      │
        │      │ CALENDAR PICKER │      │
        │      │ Select date/time│      │
        │      └─────────────────┘      │
        │               │               │
        └───────────────┴───────────────┘
                        ▼
              ✅ Success Notification
              "Post scheduled for June 15, 6:00 PM"
                        │
                        ▼
              [Return to Dashboard]
```

### Wireframe 1 : Dashboard (Desktop)

```
┌──────────────────────────────────────────────────────────────────────┐
│  [☰ Pyralys]              Search...              [Profile ▼]  [🔔]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │ 📊 124  │  │ ❤️ 2.8K │  │ 👥 +234 │  │ 📈 4.2% │                │
│  │ Posts   │  │ Likes   │  │ Followers│  │ Eng.Rate│                │
│  │ (30d)   │  │ (30d)   │  │ (30d)    │  │ (avg)   │                │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘                │
│                                                                      │
│  ┌────────────────────────────────────┐  ┌───────────────────────┐  │
│  │  Performance Overview (Last 30d)   │  │   Quick Actions       │  │
│  │  ┌────────────────────────────┐    │  │                       │  │
│  │  │     📈 Line Chart          │    │  │  [+ Create New Post]  │  │
│  │  │     (Engagement Trend)     │    │  │                       │  │
│  │  │                            │    │  │  [📅 View Calendar]    │  │
│  │  │                            │    │  │                       │  │
│  │  └────────────────────────────┘    │  │  [⚙️ Settings]         │  │
│  └────────────────────────────────────┘  │                       │  │
│                                          │  🔥 3 day streak!     │  │
│  ┌──────────────────────────────────────┐  └───────────────────────┘  │
│  │  Recent Posts                        │                         │
│  │  ┌────┬──────────┬─────────┬───────┐ │                         │
│  │  │Img │ Caption  │ Platform│ Stats │ │                         │
│  │  ├────┼──────────┼─────────┼───────┤ │                         │
│  │  │ 🖼 │ Summer...│ Insta   │ 234❤️ │ │                         │
│  │  │ 🖼 │ New prod │ TikTok  │ 1.2K❤│ │                         │
│  │  │ 🖼 │ Tips for │ LinkedIn│ 89❤️  │ │                         │
│  │  └────┴──────────┴─────────┴───────┘ │                         │
│  └──────────────────────────────────────┘                         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Wireframe 2 : Content Studio (Desktop)

```
┌──────────────────────────────────────────────────────────────────────┐
│  [← Back to Dashboard]        Content Studio                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────┐  ┌──────────────────────────────────┐  │
│  │   AI GENERATION         │  │   PREVIEW & EDIT                 │  │
│  │                         │  │                                  │  │
│  │  What do you want to    │  │  ┌────────────────────────┐      │  │
│  │  create?                │  │  │                        │      │  │
│  │  ┌────────────────────┐ │  │  │    [Image Preview]     │      │  │
│  │  │ Describe product   │ │  │  │                        │      │  │
│  │  │ or topic...        │ │  │  │    Phone mockup with   │      │  │
│  │  │                    │ │  │  │    product image       │      │  │
│  │  └────────────────────┘ │  │  │                        │      │  │
│  │                         │  │  └────────────────────────┘      │  │
│  │  Platform:              │  │  [🔄 Regenerate]                 │  │
│  │  ☑ Instagram            │  │                                  │  │
│  │  ☐ TikTok               │  │  Caption:                        │  │
│  │  ☐ Facebook             │  │  ┌────────────────────────────┐  │  │
│  │  ☐ LinkedIn             │  │  │ Discover the secret to     │  │  │
│  │                         │  │  │ radiant summer skin! ☀️🌺  │  │  │
│  │  Tone:                  │  │  │ #skincare #beauty #summer  │  │  │
│  │  ○ Casual               │  │  └────────────────────────────┘  │  │
│  │  ● Professional         │  │  [✏️ Edit]                       │  │
│  │  ○ Funny                │  │                                  │  │
│  │  ○ Inspirational        │  │  📊 Predicted Performance:       │  │
│  │                         │  │  ⭐⭐⭐⭐☆ 8.2/10                 │  │
│  │  [✨ Generate Content]  │  │  "High engagement potential"     │  │
│  │                         │  │                                  │  │
│  │  ──────────────────     │  │  Best time to post:              │  │
│  │                         │  │  📅 Today, 6:00 PM               │  │
│  │  Recent Prompts:        │  │                                  │  │
│  │  • New perfume launch   │  │  [Save Draft]  [Schedule]        │  │
│  │  • Summer sale promo    │  │              [Publish Now →]     │  │
│  │                         │  │                                  │  │
│  └─────────────────────────┘  └──────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Wireframe 3 : Analytics Dashboard

```
┌──────────────────────────────────────────────────────────────────────┐
│  Analytics                            [Date Range: Last 30 Days ▼]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Engagement Overview                                         │   │
│  │  ┌──────────────────────────────────────────────────────┐    │   │
│  │  │  📈 Multi-line Chart                                 │    │   │
│  │  │  Legend: [─ Likes] [─ Comments] [─ Shares]          │    │   │
│  │  │                                                      │    │   │
│  │  │     ^                                                │    │   │
│  │  │ 1K  │     ╱─╲                                        │    │   │
│  │  │     │    ╱   ╲     ╱╲                                │    │   │
│  │  │ 500 │   ╱     ╲   ╱  ╲  ╱╲                           │    │   │
│  │  │     │  ╱       ╲ ╱    ╲╱  ╲                          │    │   │
│  │  │   0 └──────────────────────────────────→             │    │   │
│  │  │      1   5   10  15  20  25  30 (days)              │    │   │
│  │  └──────────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌───────────────────────┐  ┌───────────────────────────────────┐   │
│  │ Top Performing Posts  │  │ Platform Breakdown                │   │
│  │                       │  │                                   │   │
│  │  1. Summer vibes 🌞   │  │  ┌────────────────────────────┐  │   │
│  │     2.4K likes        │  │  │   📊 Pie Chart             │  │   │
│  │     [View Details]    │  │  │                            │  │   │
│  │                       │  │  │   Instagram  45%           │  │   │
│  │  2. New collection    │  │  │   TikTok     35%           │  │   │
│  │     1.8K likes        │  │  │   Facebook   15%           │  │   │
│  │     [View Details]    │  │  │   LinkedIn    5%           │  │   │
│  │                       │  │  └────────────────────────────┘  │   │
│  │  3. Tutorial video    │  │                                   │   │
│  │     1.5K likes        │  │  Total Posts: 124                 │   │
│  │     [View Details]    │  │  Avg Engagement: 4.2%             │   │
│  │                       │  │                                   │   │
│  └───────────────────────┘  └───────────────────────────────────┘   │
│                                                                      │
│  [Export to PDF]  [Export to CSV]  [Share Report]                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Maquettes Détaillées

### Page : Dashboard (Détails visuels)

**Header Navigation**
- Logo Pyralys (gauche) : Gradient indigo → pink
- Search bar (centre) : Placeholder "Search posts, templates..."
- Droite :
  - Badge quota (ex: "250/1000 posts")
  - Notifications (dot rouge si nouvelles)
  - Avatar + dropdown (Settings, Billing, Logout)

**Stats Cards**
- Grid 4 colonnes (mobile : 2×2)
- Chaque card :
  - Icon colorée (top-left)
  - Métrique principale (grande typo, bold)
  - Label descriptif (petit, gray-600)
  - Trend indicator (+12% ↗, green si positif)

**Performance Chart**
- Titre "Engagement Overview" + tooltip (?)
- Tabs : 7 days | 30 days | 90 days
- Legend interactive (cliquer pour hide/show lignes)
- Hover : tooltip avec valeur exacte + date

**Quick Actions Panel**
- Card avec gradient subtil (primary-50 background)
- Bouton CTA principal : Gradient + shadow
- Secondary actions : Ghost buttons
- Streak counter : 🔥 icon + animation pulse si active

**Recent Posts Table**
- Thumbnail (60×60px, rounded)
- Caption (truncate après 40 chars)
- Platform badge (couleur brand de chaque réseau)
- Stats : compact (icons + nombres)
- Actions (hover) : Edit, Delete, Analytics

### Page : Content Studio

**Layout 2 colonnes (60/40)**

**Colonne Gauche : AI Generation**
- Textarea prompt : Placeholder avec exemple
- Chips sélectionnables pour plateformes
  - Instagram : Gradient rose-violet
  - TikTok : Noir
  - Facebook : Bleu Meta
  - LinkedIn : Bleu professionnel
- Radio buttons pour tone (avec icons)
  - 😎 Casual
  - 👔 Professional
  - 😂 Funny
  - ✨ Inspirational
- Button "Generate" : Gradient animé, disabled si prompt vide
- Loading state : Skeleton + animation shimmer
- Historique prompts : Scroll vertical, clickable

**Colonne Droite : Preview**
- Tabs pour switcher vue plateforme
- Phone mockup (Instagram style, TikTok style, etc.)
- Image preview :
  - Aspect ratio adapté à la plateforme
  - Hover : Show regenerate button overlay
- Caption editor :
  - Contenteditable avec highlighting hashtags en bleu
  - Character counter (adapté à la plateforme)
  - Emoji picker button
- Hashtags : Tags cliquables, X pour supprimer
- Prediction score :
  - Stars visual + numeric (8.2/10)
  - Color coded (red <5, yellow 5-7, green >7)
  - Tooltip avec détails prédiction

**Footer Actions**
- Sticky bottom bar
- 3 boutons : Draft | Schedule | Publish
- Schedule ouvre modal avec calendar picker

### Modal : Scheduler

```
┌─────────────────────────────────────────┐
│  📅 Schedule Post                    [X] │
├─────────────────────────────────────────┤
│                                         │
│  Select Date & Time:                    │
│  ┌─────────────────┐  ┌──────────────┐  │
│  │   June 2025     │  │  Time        │  │
│  │  M  T  W  T  F  │  │  ┌────────┐  │  │
│  │        1  2  3  │  │  │ 18:00  │  │  │
│  │  4  5  6  7  8  │  │  └────────┘  │  │
│  │  11 12 13 14 ●  │  │              │  │
│  │  (15 selected)  │  │  Timezone:   │  │
│  └─────────────────┘  │  Paris (CET) │  │
│                       └──────────────┘  │
│                                         │
│  💡 Optimal Time Suggestion:            │
│  📊 Best engagement: 18:00 - 20:00      │
│  [Use Suggestion]                       │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │ Preview: June 15, 2025 at 6:00 PM │ │
│  └────────────────────────────────────┘ │
│                                         │
│  [Cancel]              [Schedule Post] │
└─────────────────────────────────────────┘
```

---

## 5. Responsive Design

### Breakpoints
```css
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }

/* Large Desktop */
@media (min-width: 1440px) { }
```

### Mobile Adaptations

#### Dashboard Mobile
- Stats : 2×2 grid au lieu de 4 colonnes
- Chart : Swipeable carousel si plusieurs charts
- Recent posts : Cards verticales au lieu de table
- Floating Action Button (FAB) pour "Create Post"

#### Content Studio Mobile
- Layout devient vertical (1 colonne)
- Tabs pour switcher Generation ↔ Preview
- Bottom sheet pour options avancées
- Sticky header avec progress indicator

#### Navigation Mobile
- Hamburger menu (left drawer)
- Bottom nav bar (5 items max) :
  - 🏠 Home
  - ✨ Create
  - 📊 Analytics
  - 📅 Calendar
  - 👤 Profile

### Touch Interactions
- Min touch target : 44×44px (iOS guidelines)
- Swipe gestures :
  - Swipe left sur post → Quick actions (Edit, Delete)
  - Pull to refresh sur listes
  - Pinch to zoom sur images

---

## 6. Onboarding Intelligent

### First-Time User Experience (FTUE)

#### Étape 1 : Welcome Screen
```
┌─────────────────────────────────────────┐
│                                         │
│        ✨ Welcome to Pyralys!            │
│                                         │
│   Your AI-powered social media          │
│   content creation assistant            │
│                                         │
│   [Get Started →]                       │
│                                         │
└─────────────────────────────────────────┘
```

#### Étape 2 : Connect Social Accounts
```
┌─────────────────────────────────────────┐
│  Step 1 of 3: Connect Your Accounts     │
├─────────────────────────────────────────┤
│                                         │
│  Connect the platforms where you want   │
│  to publish content:                    │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │ 📷 Instagram                       │ │
│  │ Reach 2B+ users worldwide          │ │
│  │              [Connect Instagram →] │ │
│  └────────────────────────────────────┘ │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │ 🎵 TikTok                          │ │
│  │ Grow with short-form video         │ │
│  │              [Connect TikTok →]    │ │
│  └────────────────────────────────────┘ │
│                                         │
│  [Skip for Now]            [Continue →] │
└─────────────────────────────────────────┘
```

#### Étape 3 : Define Brand Voice
```
┌─────────────────────────────────────────┐
│  Step 2 of 3: Tell Us About Your Brand  │
├─────────────────────────────────────────┤
│                                         │
│  What's your brand name?                │
│  ┌────────────────────────────────────┐ │
│  │ Bella Cosmetics                    │ │
│  └────────────────────────────────────┘ │
│                                         │
│  What do you sell/promote?              │
│  ┌────────────────────────────────────┐ │
│  │ Natural skincare products          │ │
│  └────────────────────────────────────┘ │
│                                         │
│  What's your brand tone?                │
│  ○ Casual & Friendly                    │
│  ● Professional & Trustworthy           │
│  ○ Fun & Playful                        │
│  ○ Luxurious & Aspirational             │
│                                         │
│  [← Back]                  [Continue →] │
└─────────────────────────────────────────┘
```

#### Étape 4 : Create First Post
```
┌─────────────────────────────────────────┐
│  Step 3 of 3: Create Your First Post!   │
├─────────────────────────────────────────┤
│                                         │
│  Let's create content together.         │
│  Tell me what you want to promote:      │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │ Our best-selling vitamin C serum   │ │
│  │ for radiant skin                   │ │
│  └────────────────────────────────────┘ │
│                                         │
│  [✨ Generate My First Post]            │
│                                         │
│  💡 Tip: Be specific! Include details   │
│  like product benefits, target audience,│
│  or special offers.                     │
│                                         │
│  [← Back]                               │
└─────────────────────────────────────────┘
```

### Progressive Disclosure

**Première utilisation :**
- Interface simple (génération basique)
- Tooltips contextuels
- Success messages encourageants

**Après 5 posts :**
- Débloquer fonctionnalités avancées
  - Templates personnalisés
  - A/B testing suggestions
  - Analytics prédictifs détaillés

**Après 20 posts :**
- Power user features
  - Batch operations
  - API access
  - Custom workflows (Zapier)

### Tooltips et Aide Contextuelle

**Hotspots (?) sur nouveaux éléments :**
```tsx
<Tooltip content="This score predicts how well your post will perform based on AI analysis">
  <span className="text-gray-400 cursor-help">?</span>
</Tooltip>
```

**Empty States Pédagogiques :**
```
┌─────────────────────────────────────────┐
│   No posts yet!                         │
│                                         │
│   📝 Create your first post to start    │
│   building your social media presence.  │
│                                         │
│   [+ Create Your First Post]            │
│                                         │
│   Need inspiration? Check out templates │
│   [Browse Templates →]                  │
└─────────────────────────────────────────┘
```

---

## 7. Interactions et Microinteractions

### Animations et Transitions

#### Loading States

**Skeleton Loaders :**
```tsx
// components/SkeletonCard.tsx
export function SkeletonCard() {
  return (
    <div className="bg-white rounded-lg p-6 animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-2/3"></div>
    </div>
  );
}
```

**AI Generation Loading :**
- Animated gradient background
- Progress bar with steps :
  - "Analyzing prompt..." (0-25%)
  - "Generating caption..." (25-50%)
  - "Creating image..." (50-85%)
  - "Optimizing..." (85-100%)
- Estimated time remaining

**Button Loading State :**
```tsx
<button className="relative" disabled={isLoading}>
  {isLoading ? (
    <>
      <span className="opacity-0">{children}</span>
      <span className="absolute inset-0 flex items-center justify-center">
        <Spinner className="animate-spin" />
      </span>
    </>
  ) : children}
</button>
```

#### Success States

**Post Published Animation :**
```tsx
// Confetti animation + success modal
<motion.div
  initial={{ scale: 0, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{ type: "spring", duration: 0.5 }}
>
  <div className="text-center">
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 0.5 }}
    >
      ✅
    </motion.div>
    <h3>Post Published!</h3>
    <p>Your content is now live on Instagram</p>
  </div>
</motion.div>
```

**Toast Notifications :**
```tsx
// Using react-hot-toast
toast.success('Content generated successfully!', {
  icon: '✨',
  duration: 3000,
  position: 'top-right'
});
```

#### Hover Effects

**Card Hover :**
```css
.post-card {
  transition: all 0.2s ease;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}
```

**Button Hover :**
```css
.btn-primary {
  background: linear-gradient(135deg, #6366F1, #EC4899);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3);
}
```

### Drag & Drop

**Calendar Scheduling :**
```tsx
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

<DragDropContext onDragEnd={handleDragEnd}>
  <Droppable droppableId="calendar">
    {(provided) => (
      <div ref={provided.innerRef} {...provided.droppableProps}>
        {posts.map((post, index) => (
          <Draggable key={post.id} draggableId={post.id} index={index}>
            {(provided) => (
              <PostCard
                ref={provided.innerRef}
                {...provided.draggableProps}
                {...provided.dragHandleProps}
                post={post}
              />
            )}
          </Draggable>
        ))}
        {provided.placeholder}
      </div>
    )}
  </Droppable>
</DragDropContext>
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + N` | New post |
| `Ctrl/Cmd + S` | Save draft |
| `Ctrl/Cmd + Enter` | Publish now |
| `Ctrl/Cmd + K` | Quick search |
| `Escape` | Close modal |
| `?` | Show shortcuts help |

**Implementation :**
```tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
      e.preventDefault();
      openCreatePostModal();
    }
  };

  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

## 8. Accessibilité (A11y)

### Standards WCAG 2.1 (Level AA)

#### Contraste de Couleurs
- Ratio minimum 4.5:1 pour texte normal
- Ratio minimum 3:1 pour texte large (>18pt)
- Vérification avec outils (WebAIM Contrast Checker)

#### Navigation Clavier
- Tous les éléments interactifs accessibles au clavier
- Ordre de tabulation logique
- Focus visible (outline)

```css
*:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

#### ARIA Labels

```tsx
<button aria-label="Create new post">
  <PlusIcon />
</button>

<img src={post.image} alt={post.altText || "Post image"} />

<nav aria-label="Main navigation">
  <ul role="list">
    <li><a href="/dashboard">Dashboard</a></li>
  </ul>
</nav>
```

#### Screen Reader Support

```tsx
<div role="status" aria-live="polite" aria-atomic="true">
  {isGenerating && "AI is generating your content, please wait..."}
</div>

<button aria-expanded={isOpen} aria-controls="dropdown-menu">
  Options
</button>
```

#### Skip Links

```tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0 bg-primary-600 text-white p-4"
>
  Skip to main content
</a>
```

### Responsive Text Sizing
- Base font : 16px (1rem)
- Utilisateur peut zoom jusqu'à 200% sans perte de fonctionnalité
- Pas de `max-width` fixe sur containers de texte

### Dark Mode (Bonus)

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  return (
    <html lang="en" className={theme}>
      <body className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
        {children}
      </body>
    </html>
  );
}
```

```css
/* Dark mode colors */
:root.dark {
  --background: #111827;
  --foreground: #F9FAFB;
  --card: #1F2937;
  --card-foreground: #F3F4F6;
}
```

---

## 📏 Design Checklist

### Avant Développement
- [ ] Wireframes validés par stakeholders
- [ ] Design system complet (couleurs, typo, spacing)
- [ ] Maquettes haute fidélité (Figma) pour toutes les pages principales
- [ ] User flows documentés
- [ ] Responsive breakpoints définis

### Pendant Développement
- [ ] Composants UI réutilisables créés
- [ ] Animations et transitions implémentées
- [ ] Loading et error states gérés partout
- [ ] Keyboard navigation testée
- [ ] Contraste couleurs validé (WCAG AA)

### Avant Lancement
- [ ] Tests utilisateurs (5-8 personnes minimum)
- [ ] Audit accessibilité (Lighthouse, axe DevTools)
- [ ] Test cross-browser (Chrome, Firefox, Safari, Edge)
- [ ] Test responsive (mobile, tablet, desktop)
- [ ] Performance check (Core Web Vitals)

---

## ⏱️ Temps Estimés Design

| Phase | Durée | Livrables |
|-------|-------|-----------|
| **Research & Discovery** | 1 semaine | User interviews, competitive analysis |
| **Wireframes basse fidélité** | 1 semaine | 20-30 écrans wireframed |
| **Design system creation** | 1 semaine | Couleurs, typo, composants de base |
| **Maquettes haute fidélité** | 2 semaines | Figma designs complets |
| **Prototype interactif** | 1 semaine | Figma prototype clickable |
| **User testing** | 1 semaine | 5-8 sessions + rapport |
| **Itérations post-test** | 1 semaine | Ajustements basés sur feedback |
| **TOTAL** | **8 semaines** | Design production-ready |

**Designer recommandé :** 1 UX/UI designer senior (full-time)

---

## 🎨 Outils Recommandés

- **Design :** Figma (collaborative, prototyping)
- **Icons :** Heroicons, Lucide Icons
- **Illustrations :** unDraw, Storyset
- **Animations :** Framer Motion, GSAP
- **Accessibility :** axe DevTools, WAVE
- **Color :** Coolors.co, Adobe Color
- **Fonts :** Google Fonts (Inter, Plus Jakarta Sans)

---

**Dernière mise à jour :** 31 Décembre 2025
**Auteur :** Équipe Design Pyralys
**Version :** 1.0
