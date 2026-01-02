# 🚀 Guide de Démarrage Rapide - Pyralys

Guide pour lancer et visualiser l'application Pyralys en 5 minutes !

## Prérequis

- **Docker Desktop** installé ([Télécharger ici](https://www.docker.com/products/docker-desktop))
- **Git** installé
- **Au moins 4GB de RAM disponible**

## 🏃 Démarrage Ultra-Rapide (Docker)

### 1. Cloner le projet (si pas déjà fait)

```bash
git clone https://github.com/westekey/Pyralys.git
cd Pyralys
```

### 2. Vérifier les fichiers de configuration

Les fichiers `.env` ont déjà été créés pour vous :
- ✅ `backend/.env` - Configuration backend
- ✅ `frontend/.env.local` - Configuration frontend

**Note :** Les clés API (OpenAI, Stripe, etc.) sont optionnelles pour visualiser l'interface !

### 3. Lancer tous les services

```bash
# Lancer tous les services Docker
docker-compose up -d

# Attendre que tous les services démarrent (30-60 secondes)
# Vérifier le statut
docker-compose ps
```

Vous devriez voir ces services en "Up" :
- ✅ pyralys-postgres (base de données)
- ✅ pyralys-redis (cache)
- ✅ pyralys-backend (API FastAPI)
- ✅ pyralys-frontend (Next.js)
- ✅ pyralys-celery-worker (tâches async)
- ✅ pyralys-celery-beat (planificateur)
- ✅ pyralys-flower (monitoring Celery)
- ✅ pyralys-wordpress (CMS)
- ✅ pyralys-wordpress-mysql (BD WordPress)

### 4. Initialiser la base de données

```bash
# Lancer les migrations Alembic
docker-compose exec backend alembic upgrade head
```

### 5. Créer un utilisateur test (optionnel)

```bash
# Accéder au container backend
docker-compose exec backend python

# Dans le shell Python :
```
```python
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import uuid

db = SessionLocal()
user = User(
    id=uuid.uuid4(),
    email="demo@pyralys.com",
    hashed_password=get_password_hash("demo123"),
    full_name="Demo User",
    plan_type="premium"
)
db.add(user)
db.commit()
print(f"✅ User created: {user.email}")
exit()
```

## 🌐 Accéder à l'application

Ouvrez votre navigateur et accédez à :

### 🎨 Frontend (Interface Utilisateur)
```
http://localhost:3000
```
**Ce que vous pouvez faire :**
- ✅ Créer un compte / Se connecter
- ✅ Voir le dashboard
- ✅ Créer des posts
- ✅ Voir l'interface de génération AI
- ✅ Accéder à la page Analytics
- ✅ Voir les plans de tarification

**Compte de test :**
- Email: `demo@pyralys.com`
- Password: `demo123`

### 📚 API Documentation (Swagger)
```
http://localhost:8000/docs
```
**Ce que vous pouvez faire :**
- ✅ Explorer tous les endpoints API (35+)
- ✅ Tester les requêtes directement
- ✅ Voir les schémas de données
- ✅ Tester l'authentification

### 🔧 Backend API
```
http://localhost:8000
```
**Health check :**
```
http://localhost:8000/health
```

### 🌸 Flower (Monitoring Celery)
```
http://localhost:5555
```
**Ce que vous pouvez voir :**
- ✅ Workers actifs
- ✅ Tâches en cours
- ✅ Historique des tâches
- ✅ Statistiques

### 📝 WordPress
```
http://localhost:8080
```
**Ce que vous pouvez faire :**
- ✅ Configurer WordPress
- ✅ Tester la publication depuis Pyralys

### 🗄️ phpMyAdmin
```
http://localhost:8081
```
**Accès :**
- Server: `wordpress_mysql`
- Username: `wordpress`
- Password: `wordpress123`

## 📱 Pages Disponibles

### Frontend

1. **Page d'Accueil**
   - URL: `http://localhost:3000/`

2. **Inscription**
   - URL: `http://localhost:3000/register`
   - Créez votre compte gratuitement

3. **Connexion**
   - URL: `http://localhost:3000/login`
   - Connectez-vous avec votre compte

4. **Dashboard**
   - URL: `http://localhost:3000/dashboard`
   - Vue d'ensemble de vos statistiques

5. **Gestion de Contenu**
   - URL: `http://localhost:3000/dashboard/content`
   - Créer, éditer, publier des posts
   - Voir l'historique de publication

6. **Analytics**
   - URL: `http://localhost:3000/dashboard/analytics`
   - Métriques de performance
   - Graphiques et statistiques
   - Top posts

7. **Facturation**
   - URL: `http://localhost:3000/dashboard/billing`
   - Voir les plans
   - Gérer l'abonnement
   - Historique de facturation

## 🧪 Tester les Fonctionnalités

### Sans clés API (Interface seulement)

Vous pouvez visualiser **toute l'interface** sans aucune clé API :
- ✅ Dashboard
- ✅ Page de création de posts
- ✅ Page Analytics
- ✅ Page Billing
- ✅ Toutes les UI/UX

### Avec clés API (Fonctionnalités complètes)

Pour tester les fonctionnalités AI et publication :

#### 1. OpenAI (Génération de captions et images)

Éditez `backend/.env` :
```env
OPENAI_API_KEY=sk-votre-cle-openai-ici
```

Puis redémarrez :
```bash
docker-compose restart backend
```

**Testez :**
- Génération de captions AI
- Génération d'images avec DALL-E

#### 2. Stripe (Paiements)

Éditez `backend/.env` et `frontend/.env.local` :
```env
# Backend
STRIPE_SECRET_KEY=sk_test_votre-cle
STRIPE_WEBHOOK_SECRET=whsec_votre-secret

# Frontend
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_votre-cle
```

Redémarrez :
```bash
docker-compose restart backend frontend
```

**Testez :**
- Checkout pour upgrade de plan
- Customer portal

#### 3. Instagram (Publication)

1. Créer une app Facebook/Instagram sur [developers.facebook.com](https://developers.facebook.com)
2. Configurer OAuth redirect: `http://localhost:8000/api/v1/auth/instagram/callback`
3. Mettre les clés dans `backend/.env`

**Testez :**
- Connexion Instagram
- Publication de posts

## 📊 Voir les Logs

### Logs en temps réel de tous les services
```bash
docker-compose logs -f
```

### Logs d'un service spécifique
```bash
# Backend
docker-compose logs -f backend

# Frontend
docker-compose logs -f frontend

# Celery Worker
docker-compose logs -f celery_worker

# PostgreSQL
docker-compose logs -f postgres
```

## 🛑 Arrêter les services

```bash
# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker-compose down -v
```

## 🔄 Redémarrer après modifications

```bash
# Redémarrer un service spécifique
docker-compose restart backend

# Reconstruire après changement de code
docker-compose up -d --build

# Reconstruire seulement le backend
docker-compose up -d --build backend
```

## 🐛 Résolution de Problèmes

### Les services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier l'état des containers
docker-compose ps

# Redémarrer complètement
docker-compose down
docker-compose up -d
```

### Le frontend affiche une erreur

```bash
# Vérifier que le backend est accessible
curl http://localhost:8000/health

# Redémarrer le frontend
docker-compose restart frontend

# Voir les logs
docker-compose logs -f frontend
```

### La base de données n'est pas accessible

```bash
# Vérifier PostgreSQL
docker-compose logs postgres

# Vérifier la connexion
docker-compose exec postgres pg_isready -U pyralys

# Relancer les migrations
docker-compose exec backend alembic upgrade head
```

### Port déjà utilisé

Si un port est déjà utilisé (3000, 8000, etc.) :
```bash
# Voir les processus utilisant le port
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Modifier les ports dans docker-compose.yml si nécessaire
```

## 📸 Captures d'écran attendues

Une fois lancé, vous devriez voir :

### Frontend (localhost:3000)
- ✅ Page de login élégante
- ✅ Dashboard avec statistiques
- ✅ Bibliothèque de contenu
- ✅ Interface de création de posts
- ✅ Dashboard analytics avec graphiques
- ✅ Page de tarification (4 plans)

### API Docs (localhost:8000/docs)
- ✅ Documentation Swagger interactive
- ✅ 35+ endpoints organisés par catégorie
- ✅ Schémas de données
- ✅ Bouton "Try it out" pour tester

### Flower (localhost:5555)
- ✅ Workers Celery actifs
- ✅ Queue de tâches
- ✅ Statistiques de performance

## 🎯 Prochaines Étapes

Une fois que vous visualisez l'application :

1. **Explorer l'interface** - Naviguez dans toutes les pages
2. **Créer des posts** - Testez la création de contenu
3. **Voir les analytics** - Explorez le dashboard
4. **Tester l'API** - Utilisez Swagger à `/docs`
5. **Configurer les clés API** - Pour tester les fonctionnalités complètes

## 📚 Documentation Complète

- **API Testing Guide** - Voir [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
- **Production Deployment** - Voir [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Summary** - Voir [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## ❓ Besoin d'Aide ?

- **Issues GitHub** : https://github.com/westekey/Pyralys/issues
- **Documentation API** : http://localhost:8000/docs
- **Logs** : `docker-compose logs -f`

---

**Bon développement ! 🚀**

*Si tout fonctionne, vous devriez voir l'application sur http://localhost:3000 dans les 2 minutes suivant `docker-compose up -d`*
