# 🛠️ Setup Guide - Pyralys

Guide complet pour configurer et démarrer le projet Pyralys en local.

---

## 📋 Prérequis

### Obligatoire
- **Docker Desktop** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**

### Optionnel (pour développement sans Docker)
- **Python 3.11+**
- **Node.js 20+**
- **PostgreSQL 15+**
- **Redis 7+**

---

## 🚀 Démarrage Rapide (avec Docker)

### 1. Cloner le Repository

```bash
git clone https://github.com/westekey/Pyralys.git
cd Pyralys
```

### 2. Configuration Initiale

```bash
make setup
```

Cette commande :
- Copie `backend/.env.example` vers `backend/.env`
- Copie `frontend/.env.example` vers `frontend/.env.local`

### 3. Configurer les Variables d'Environnement

#### Backend `.env`

Éditer `backend/.env` et remplir au minimum :

```env
# Required
SECRET_KEY=votre-secret-key-super-securisee
JWT_SECRET=votre-jwt-secret-key

# OpenAI (obligatoire pour AI features)
OPENAI_API_KEY=sk-votre-cle-openai

# Optionnel pour MVP
FACEBOOK_APP_ID=votre-facebook-app-id
FACEBOOK_APP_SECRET=votre-facebook-app-secret
STRIPE_SECRET_KEY=sk_test_votre-cle-stripe
```

#### Frontend `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_votre-cle-publique
```

### 4. Démarrer l'Environnement

```bash
make dev
```

Cette commande démarre tous les services :
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)
- Celery Worker
- Celery Beat
- Flower (port 5555)

### 5. Accéder à l'Application

Ouvrez votre navigateur :

- **Frontend** : http://localhost:3000
- **Backend API Docs** : http://localhost:8000/api/docs
- **Flower (Celery monitoring)** : http://localhost:5555

---

## 📊 Vérification de l'Installation

### Health Check Backend

```bash
curl http://localhost:8000/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### Test Frontend

Visitez http://localhost:3000 - vous devriez voir la landing page.

---

## 🗄️ Database Setup

### Migrations Initiales

```bash
make migrate
```

Cette commande exécute toutes les migrations Alembic.

### Créer une Nouvelle Migration

```bash
docker-compose exec backend alembic revision --autogenerate -m "Description du changement"
```

### Appliquer les Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### Revenir en Arrière

```bash
docker-compose exec backend alembic downgrade -1
```

---

## 🧪 Tests

### Backend Tests

```bash
# Tous les tests
docker-compose exec backend pytest

# Avec coverage
docker-compose exec backend pytest --cov=app tests/

# Tests spécifiques
docker-compose exec backend pytest tests/test_auth.py -v
```

### Frontend Tests

```bash
# Tests unitaires
docker-compose exec frontend npm test

# Tests E2E
docker-compose exec frontend npm run test:e2e
```

---

## 🛠️ Commandes Utiles

### Voir les Logs

```bash
# Tous les services
make logs

# Service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Accéder aux Shells

```bash
# Backend shell
make backend-shell

# Frontend shell
make frontend-shell

# Database shell
make db-shell
```

### Arrêter les Services

```bash
make down
```

### Nettoyer Complètement

⚠️ **Attention** : Supprime tous les volumes (données perdues)

```bash
make clean
```

---

## 🔧 Configuration Avancée

### AWS S3 (Media Storage)

1. Créer un bucket S3
2. Créer un IAM user avec accès S3
3. Ajouter dans `backend/.env` :

```env
AWS_ACCESS_KEY_ID=votre-access-key
AWS_SECRET_ACCESS_KEY=votre-secret-key
AWS_REGION=eu-west-1
AWS_S3_BUCKET=pyralys-media-dev
```

### Stripe (Billing)

1. Créer un compte Stripe (test mode)
2. Obtenir les clés API
3. Configurer les webhooks :
   - URL : `http://localhost:8000/api/v1/billing/webhooks/stripe`
   - Events : `checkout.session.completed`, `customer.subscription.deleted`

### Instagram API

1. Créer une app Facebook Developer
2. Configurer Instagram Basic Display
3. Ajouter dans `backend/.env` :

```env
FACEBOOK_APP_ID=votre-app-id
FACEBOOK_APP_SECRET=votre-app-secret
```

---

## 🐛 Troubleshooting

### Port Déjà Utilisé

Si un port est déjà utilisé, modifier dans `docker-compose.yml` :

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change 8000 to 8001
```

### Problème de Permissions Docker

Sur Linux :

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Base de Données ne Démarre Pas

Vérifier les logs :

```bash
docker-compose logs postgres
```

Nettoyer et redémarrer :

```bash
make clean
make dev
```

### Backend API 500 Errors

Vérifier les variables d'environnement :

```bash
docker-compose exec backend env | grep -i secret
```

---

## 📝 Next Steps

Une fois l'environnement configuré :

1. ✅ Vérifier que tous les services fonctionnent
2. ✅ Créer un compte utilisateur via l'interface
3. ✅ Tester la génération AI
4. ✅ Explorer l'API documentation

Pour le développement, consultez :
- [Documentation Architecture](docs/02-ARCHITECTURE-TECHNIQUE.md)
- [Plan de Développement MVP](docs/04-PLAN-DEVELOPPEMENT-MVP.md)

---

## 💬 Support

Problèmes ? Créez une [issue](https://github.com/westekey/Pyralys/issues).

---

**Happy Coding! 🚀**
