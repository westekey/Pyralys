# 🛠️ Installation Manuelle - Pyralys (Sans Docker)

Guide complet pour installer et lancer Pyralys sans Docker.

## 📋 Prérequis à Installer

### 1. Python 3.11+
**Windows :**
- Télécharger : https://www.python.org/downloads/
- Cocher "Add Python to PATH" lors de l'installation

**Mac :**
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

Vérifier :
```bash
python --version  # ou python3 --version
# Doit afficher Python 3.11.x ou supérieur
```

### 2. Node.js 20+
**Toutes plateformes :**
- Télécharger : https://nodejs.org/ (version LTS)

**Ou avec gestionnaire de versions (recommandé) :**
```bash
# nvm (Mac/Linux)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# nvm-windows (Windows)
# Télécharger depuis : https://github.com/coreybutler/nvm-windows/releases
```

Vérifier :
```bash
node --version  # v20.x.x
npm --version   # 10.x.x
```

### 3. PostgreSQL 15+
**Windows :**
- Télécharger : https://www.postgresql.org/download/windows/
- Installer avec les paramètres par défaut
- Noter le mot de passe du superuser

**Mac :**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Vérifier :
```bash
psql --version  # PostgreSQL 15.x
```

### 4. Redis 7+
**Windows :**
- Télécharger depuis : https://github.com/microsoftarchive/redis/releases
- Ou utiliser WSL2 et installer comme Linux

**Mac :**
```bash
brew install redis
brew services start redis
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

Vérifier :
```bash
redis-cli ping  # Doit répondre PONG
```

## 🗄️ Configuration de la Base de Données

### 1. Créer la base de données PostgreSQL

```bash
# Se connecter à PostgreSQL
# Windows/Mac : psql -U postgres
# Linux : sudo -u postgres psql

# Dans le prompt PostgreSQL :
CREATE DATABASE pyralys_dev;
CREATE USER pyralys WITH PASSWORD 'pyralys_dev_password';
GRANT ALL PRIVILEGES ON DATABASE pyralys_dev TO pyralys;
\q
```

### 2. Vérifier la connexion

```bash
psql -U pyralys -d pyralys_dev -h localhost
# Entrer le mot de passe : pyralys_dev_password
# Si connecté avec succès, taper \q pour quitter
```

## 🔧 Configuration Backend

### 1. Naviguer vers le backend

```bash
cd /chemin/vers/Pyralys/backend
```

### 2. Créer un environnement virtuel Python

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows :
venv\Scripts\activate

# Mac/Linux :
source venv/bin/activate
```

Votre prompt devrait maintenant afficher `(venv)`.

### 3. Installer les dépendances Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Cela prendra quelques minutes pour installer tous les packages.

### 4. Configurer les variables d'environnement

Le fichier `backend/.env` existe déjà, mais vérifiez qu'il contient :

```env
# Application
APP_NAME=Pyralys API
APP_ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production-12345678901234567890
JWT_SECRET=dev-jwt-secret-key-change-in-production-12345678901234567890

# Database (local configuration)
DATABASE_URL=postgresql+asyncpg://pyralys:pyralys_dev_password@localhost:5432/pyralys_dev

# Redis (local configuration)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI (OPTIONNEL - pour tester l'IA)
OPENAI_API_KEY=sk-YOUR-KEY-HERE-OPTIONAL

# Stripe (OPTIONNEL - mode test)
STRIPE_SECRET_KEY=sk_test_YOUR-KEY-HERE-OPTIONAL
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR-KEY-HERE-OPTIONAL

# Frontend
FRONTEND_URL=http://localhost:3000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Initialiser la base de données avec Alembic

```bash
# Lancer les migrations
alembic upgrade head
```

Vous devriez voir :
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, Add subscription and platform tables
```

### 6. Créer un utilisateur de test

```bash
# Lancer Python
python

# Dans le shell Python, copier-coller :
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
print(f"✅ Utilisateur créé : {user.email}")
db.close()
exit()
```

### 7. Lancer le serveur backend

```bash
# Dans le terminal backend (avec venv activé)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Vous devriez voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Tester :** Ouvrir http://localhost:8000/health dans votre navigateur
Vous devriez voir : `{"status":"healthy","timestamp":"..."}`

**Laisser ce terminal ouvert** - le backend est maintenant actif.

## 🎨 Configuration Frontend

### 1. Ouvrir un NOUVEAU terminal

### 2. Naviguer vers le frontend

```bash
cd /chemin/vers/Pyralys/frontend
```

### 3. Installer les dépendances Node.js

```bash
npm install
```

Cela prendra quelques minutes.

### 4. Vérifier les variables d'environnement

Le fichier `frontend/.env.local` existe déjà, vérifiez qu'il contient :

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# App Configuration
NEXT_PUBLIC_APP_NAME=Pyralys
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Stripe (OPTIONNEL)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR-KEY-HERE-OPTIONAL
```

### 5. Lancer le serveur frontend

```bash
npm run dev
```

Vous devriez voir :
```
   ▲ Next.js 14.x.x
   - Local:        http://localhost:3000
   - Ready in 2.5s
```

**✅ Tester :** Ouvrir http://localhost:3000 dans votre navigateur
Vous devriez voir la page d'accueil de Pyralys !

**Laisser ce terminal ouvert** - le frontend est maintenant actif.

## 🔄 Lancer Celery (Tâches en arrière-plan) - OPTIONNEL

Pour tester les fonctionnalités de publication et scheduling, vous avez besoin de Celery.

### 1. Ouvrir un 3ème terminal

### 2. Activer l'environnement Python

```bash
cd /chemin/vers/Pyralys/backend
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Lancer Celery Worker

```bash
celery -A app.celery_app worker --loglevel=info
```

### 4. (Optionnel) Lancer Celery Beat dans un 4ème terminal

Pour les tâches planifiées :

```bash
cd /chemin/vers/Pyralys/backend
source venv/bin/activate
celery -A app.celery_app beat --loglevel=info
```

## 🌐 Accès aux Services

Une fois tout lancé, vous pouvez accéder à :

| Service | URL | Description |
|---------|-----|-------------|
| **🎨 Frontend** | http://localhost:3000 | Interface utilisateur |
| **📚 API Docs** | http://localhost:8000/docs | Documentation Swagger |
| **🔧 API** | http://localhost:8000 | Backend API |
| **✅ Health Check** | http://localhost:8000/health | Vérification backend |

## 📱 Pages Disponibles

1. **Page d'accueil** : http://localhost:3000
2. **Inscription** : http://localhost:3000/register
3. **Connexion** : http://localhost:3000/login
   - Email: `demo@pyralys.com`
   - Password: `demo123`
4. **Dashboard** : http://localhost:3000/dashboard
5. **Contenu** : http://localhost:3000/dashboard/content
6. **Analytics** : http://localhost:3000/dashboard/analytics
7. **Billing** : http://localhost:3000/dashboard/billing

## ✅ Résumé des Terminaux Nécessaires

Pour une expérience complète, vous devez avoir ces terminaux ouverts :

1. **Terminal 1 (Backend)** :
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Terminal 2 (Frontend)** :
   ```bash
   cd frontend
   npm run dev
   ```

3. **Terminal 3 (Celery Worker - Optionnel)** :
   ```bash
   cd backend
   source venv/bin/activate
   celery -A app.celery_app worker --loglevel=info
   ```

4. **Terminal 4 (Celery Beat - Optionnel)** :
   ```bash
   cd backend
   source venv/bin/activate
   celery -A app.celery_app beat --loglevel=info
   ```

## 🐛 Résolution de Problèmes

### Erreur : "ModuleNotFoundError"
```bash
# Vérifier que venv est activé (vous devez voir (venv) dans le prompt)
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur : "Database connection failed"
```bash
# Vérifier que PostgreSQL est lancé
# Windows : Services → PostgreSQL
# Mac : brew services list
# Linux : sudo systemctl status postgresql

# Vérifier les credentials dans .env
# DATABASE_URL=postgresql+asyncpg://pyralys:pyralys_dev_password@localhost:5432/pyralys_dev
```

### Erreur : "Redis connection failed"
```bash
# Vérifier que Redis est lancé
redis-cli ping  # Doit répondre PONG

# Démarrer Redis si nécessaire
# Mac : brew services start redis
# Linux : sudo systemctl start redis-server
# Windows : Lancer redis-server.exe
```

### Port 3000 ou 8000 déjà utilisé
```bash
# Trouver le processus utilisant le port
# Windows :
netstat -ano | findstr :3000

# Mac/Linux :
lsof -i :3000

# Tuer le processus ou utiliser un autre port
# Backend sur port 8001 :
uvicorn app.main:app --reload --port 8001

# Puis mettre à jour frontend/.env.local :
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
```

### Le frontend ne se connecte pas au backend
```bash
# 1. Vérifier que le backend répond
curl http://localhost:8000/health

# 2. Vérifier CORS dans backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# 3. Redémarrer le backend
# Ctrl+C dans le terminal backend puis relancer uvicorn
```

## 🎯 Prochaines Étapes

1. **Se connecter** avec demo@pyralys.com / demo123
2. **Explorer le Dashboard**
3. **Créer un post** dans la section Content
4. **Voir les Analytics**
5. **Tester l'API** sur http://localhost:8000/docs

## 🔑 Activer les Fonctionnalités Complètes

Pour tester l'IA et la publication, ajoutez vos clés API dans `backend/.env` :

```env
# Pour la génération de captions et images AI
OPENAI_API_KEY=sk-votre-cle-openai-ici

# Pour les paiements (mode test)
STRIPE_SECRET_KEY=sk_test_votre-cle
STRIPE_PUBLISHABLE_KEY=pk_test_votre-cle

# Pour Instagram
FACEBOOK_APP_ID=votre-app-id
FACEBOOK_APP_SECRET=votre-secret
```

Puis redémarrez le backend (Ctrl+C et relancer uvicorn).

## 📚 Besoin d'Aide ?

- **API Documentation** : http://localhost:8000/docs
- **Logs Backend** : Visibles dans le terminal 1
- **Logs Frontend** : Visibles dans le terminal 2
- **Guide complet** : Voir [QUICK_START.md](QUICK_START.md)

---

**Bon développement ! 🚀**

Une fois tout lancé, l'application sera accessible sur http://localhost:3000
