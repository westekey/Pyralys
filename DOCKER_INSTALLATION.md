# 🐳 Installation de Docker et Lancement de Pyralys

Guide complet pour installer Docker et lancer Pyralys en quelques minutes !

## 📥 Installation de Docker Desktop

Docker Desktop inclut Docker et Docker Compose - tout ce dont vous avez besoin.

### 🪟 Windows

**Configuration requise :**
- Windows 10/11 (64-bit)
- Au moins 4GB de RAM
- WSL 2 (sera installé automatiquement)

**Étapes d'installation :**

1. **Télécharger Docker Desktop pour Windows**

   🔗 **Lien direct :** https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

   Ou visitez : https://www.docker.com/products/docker-desktop/

2. **Installer Docker Desktop**
   - Double-cliquer sur `Docker Desktop Installer.exe`
   - Suivre l'assistant d'installation
   - ✅ Cocher "Use WSL 2 instead of Hyper-V" (recommandé)
   - ✅ Cocher "Add shortcut to desktop"
   - Cliquer sur "Ok" puis "Install"

3. **Redémarrer votre ordinateur**
   - L'installation vous demandera de redémarrer

4. **Lancer Docker Desktop**
   - Chercher "Docker Desktop" dans le menu Démarrer
   - Double-cliquer pour lancer
   - Accepter les termes et conditions
   - Vous pouvez créer un compte Docker (optionnel) ou cliquer "Skip"

5. **Vérifier l'installation**
   - Ouvrir PowerShell ou CMD
   ```powershell
   docker --version
   docker-compose --version
   ```

   Vous devriez voir :
   ```
   Docker version 24.x.x, build ...
   Docker Compose version v2.x.x
   ```

**✅ Docker est maintenant installé sur Windows !**

---

### 🍎 macOS

**Configuration requise :**
- macOS 11 Big Sur ou plus récent
- Mac avec processeur Intel OU Apple Silicon (M1/M2/M3)
- Au moins 4GB de RAM

**Étapes d'installation :**

1. **Choisir la version selon votre processeur**

   **Pour Mac Intel :**

   🔗 **Lien direct :** https://desktop.docker.com/mac/main/amd64/Docker.dmg

   **Pour Mac Apple Silicon (M1/M2/M3) :**

   🔗 **Lien direct :** https://desktop.docker.com/mac/main/arm64/Docker.dmg

   Ou visitez : https://www.docker.com/products/docker-desktop/

2. **Installer Docker Desktop**
   - Ouvrir le fichier `Docker.dmg` téléchargé
   - Glisser l'icône Docker vers le dossier Applications
   - Ouvrir le dossier Applications
   - Double-cliquer sur Docker pour le lancer

3. **Première configuration**
   - Entrer votre mot de passe macOS pour autoriser l'installation
   - Accepter les termes et conditions
   - Vous pouvez créer un compte Docker (optionnel) ou cliquer "Skip"

4. **Vérifier l'installation**
   - Ouvrir Terminal
   ```bash
   docker --version
   docker-compose --version
   ```

   Vous devriez voir :
   ```
   Docker version 24.x.x, build ...
   Docker Compose version v2.x.x
   ```

**✅ Docker est maintenant installé sur Mac !**

---

### 🐧 Linux (Ubuntu/Debian)

**Configuration requise :**
- Ubuntu 20.04+ ou Debian 10+
- 64-bit
- Au moins 4GB de RAM

**Méthode 1 : Installation automatique (recommandée)**

```bash
# Télécharger et exécuter le script d'installation Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter votre utilisateur au groupe docker (pour éviter sudo)
sudo usermod -aG docker $USER

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Redémarrer la session (ou redémarrer l'ordinateur)
newgrp docker

# Vérifier l'installation
docker --version
docker-compose --version
```

**Méthode 2 : Installation manuelle (Ubuntu)**

```bash
# Mettre à jour les packages
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Ajouter la clé GPG Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Ajouter le repository Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Redémarrer la session
newgrp docker

# Vérifier l'installation
docker --version
docker compose version
```

**✅ Docker est maintenant installé sur Linux !**

---

## 🚀 Lancer Pyralys avec Docker

Maintenant que Docker est installé, voici comment lancer Pyralys :

### Étape 1 : Cloner le projet (si pas déjà fait)

```bash
# Cloner depuis GitHub
git clone https://github.com/westekey/Pyralys.git

# Aller dans le dossier
cd Pyralys
```

### Étape 2 : Vérifier que Docker fonctionne

```bash
# Tester Docker
docker run hello-world
```

Si vous voyez "Hello from Docker!", tout est bon ! ✅

### Étape 3 : Lancer tous les services

```bash
# Lancer tous les containers en arrière-plan
docker-compose up -d
```

**Ce que cette commande fait :**
- 📦 Télécharge toutes les images Docker nécessaires (première fois uniquement - peut prendre 5-10 minutes)
- 🚀 Lance PostgreSQL (base de données)
- 🚀 Lance Redis (cache)
- 🚀 Lance le Backend (API FastAPI)
- 🚀 Lance le Frontend (Next.js)
- 🚀 Lance Celery Worker (tâches async)
- 🚀 Lance Celery Beat (planificateur)
- 🚀 Lance Flower (monitoring)
- 🚀 Lance WordPress + MySQL

**Première exécution :** Cela peut prendre 5-10 minutes pour tout télécharger et démarrer.

**Exécutions suivantes :** 30 secondes seulement !

### Étape 4 : Vérifier que tout fonctionne

```bash
# Voir le statut des services
docker-compose ps
```

Vous devriez voir tous les services avec "Up" :
```
NAME                        STATUS
pyralys-backend             Up
pyralys-celery-beat         Up
pyralys-celery-worker       Up
pyralys-flower              Up
pyralys-frontend            Up
pyralys-postgres            Up
pyralys-redis               Up
pyralys-wordpress           Up
pyralys-wordpress-mysql     Up
```

### Étape 5 : Initialiser la base de données

```bash
# Lancer les migrations Alembic
docker-compose exec backend alembic upgrade head
```

Vous devriez voir :
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, Add subscription...
```

### Étape 6 : Créer un utilisateur de test (optionnel)

```bash
# Accéder au container backend
docker-compose exec backend python
```

Dans le shell Python, copier-coller :
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

### Étape 7 : Accéder à l'application !

**🎉 C'est prêt !** Ouvrez votre navigateur :

| Service | URL | Description |
|---------|-----|-------------|
| **🎨 Frontend** | http://localhost:3000 | Interface utilisateur |
| **🔐 Login** | http://localhost:3000/login | Page de connexion |
| **📚 API Docs** | http://localhost:8000/docs | Documentation Swagger |
| **✅ Health** | http://localhost:8000/health | Vérification backend |
| **🌸 Flower** | http://localhost:5555 | Monitoring Celery |
| **📝 WordPress** | http://localhost:8080 | WordPress de test |
| **🗄️ phpMyAdmin** | http://localhost:8081 | Base de données WP |

### 🔐 Se Connecter

1. Aller sur **http://localhost:3000/login**
2. Email : `demo@pyralys.com`
3. Password : `demo123`
4. Cliquer sur "Login"

**🎉 Vous êtes maintenant dans Pyralys !**

---

## 📱 Pages à Explorer

Une fois connecté, explorez :

1. **Dashboard** - http://localhost:3000/dashboard
   - Vue d'ensemble avec statistiques
   - Métriques de performance

2. **Contenu** - http://localhost:3000/dashboard/content
   - Créer des posts
   - Gérer vos publications
   - Voir l'historique

3. **Analytics** - http://localhost:3000/dashboard/analytics
   - Graphiques de performance
   - Top posts
   - Insights par plateforme

4. **Billing** - http://localhost:3000/dashboard/billing
   - Plans tarifaires
   - Gestion abonnement
   - Historique de facturation

---

## 📊 Commandes Docker Utiles

### Voir les logs en temps réel

```bash
# Tous les services
docker-compose logs -f

# Un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery_worker
```

### Arrêter les services

```bash
# Arrêter tous les containers (données conservées)
docker-compose down

# Arrêter ET supprimer les volumes (⚠️ supprime toutes les données)
docker-compose down -v
```

### Redémarrer les services

```bash
# Redémarrer tous les services
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart backend
docker-compose restart frontend
```

### Reconstruire après modification de code

```bash
# Reconstruire et redémarrer
docker-compose up -d --build

# Reconstruire seulement le backend
docker-compose up -d --build backend
```

### Voir l'utilisation des ressources

```bash
docker stats
```

### Nettoyer Docker (libérer de l'espace)

```bash
# Supprimer les containers arrêtés
docker container prune

# Supprimer les images inutilisées
docker image prune

# Tout nettoyer (⚠️ attention)
docker system prune -a
```

---

## 🐛 Résolution de Problèmes

### Docker Desktop ne démarre pas (Windows)

**Problème :** "Docker Desktop requires a newer WSL kernel version"

**Solution :**
```powershell
# Mettre à jour WSL
wsl --update

# Redémarrer Docker Desktop
```

### Les services ne démarrent pas

```bash
# Voir les logs pour identifier le problème
docker-compose logs

# Redémarrer complètement
docker-compose down
docker-compose up -d
```

### Port 3000 ou 8000 déjà utilisé

**Solution 1 : Arrêter le processus utilisant le port**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :3000
kill -9 <PID>
```

**Solution 2 : Modifier les ports dans docker-compose.yml**
```yaml
# Changer les ports exposés
ports:
  - "3001:3000"  # Accéder via localhost:3001
```

### Erreur "Cannot connect to Docker daemon"

```bash
# S'assurer que Docker Desktop est lancé
# Windows/Mac : Lancer Docker Desktop depuis le menu
# Linux :
sudo systemctl start docker
```

### Base de données vide après redémarrage

```bash
# Vérifier que les volumes existent
docker volume ls

# Relancer les migrations si nécessaire
docker-compose exec backend alembic upgrade head
```

### Le frontend affiche "Cannot connect to backend"

```bash
# Vérifier que le backend est accessible
curl http://localhost:8000/health

# Vérifier les logs du backend
docker-compose logs backend

# Redémarrer le backend
docker-compose restart backend
```

### Images Docker corrompues

```bash
# Reconstruire complètement
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔄 Workflow de Développement

### Développement quotidien

```bash
# Matin : Lancer tout
docker-compose up -d

# Travailler sur le code
# Les changements sont automatiquement détectés (hot-reload)

# Voir les logs pendant le dev
docker-compose logs -f backend frontend

# Soir : Arrêter
docker-compose down
```

### Après modification du code

**Backend (Python) :**
- Les changements sont automatiques grâce à `--reload`
- Si vous modifiez `requirements.txt` :
  ```bash
  docker-compose up -d --build backend
  ```

**Frontend (Next.js) :**
- Les changements sont automatiques (Fast Refresh)
- Si vous modifiez `package.json` :
  ```bash
  docker-compose up -d --build frontend
  ```

**Migrations de base de données :**
```bash
# Créer une nouvelle migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Appliquer les migrations
docker-compose exec backend alembic upgrade head
```

---

## 🎓 Ressources Supplémentaires

### Documentation Docker
- **Site officiel :** https://docs.docker.com/
- **Docker Compose :** https://docs.docker.com/compose/
- **Tutoriels :** https://www.docker.com/get-started/

### Documentation Pyralys
- **Quick Start :** [QUICK_START.md](QUICK_START.md)
- **API Testing :** [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
- **Deployment :** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Summary :** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## ✅ Checklist de Démarrage

- [ ] Docker Desktop installé et lancé
- [ ] `docker --version` fonctionne
- [ ] `docker-compose --version` fonctionne
- [ ] `git clone` du projet Pyralys
- [ ] `docker-compose up -d` exécuté
- [ ] Migrations appliquées (`alembic upgrade head`)
- [ ] Utilisateur de test créé
- [ ] http://localhost:3000 accessible
- [ ] Login avec demo@pyralys.com fonctionne
- [ ] Dashboard visible

---

## 🎉 Félicitations !

Si vous avez suivi toutes les étapes, vous avez maintenant :
- ✅ Docker installé et configuré
- ✅ Pyralys fonctionnel sur votre machine
- ✅ Tous les services actifs (backend, frontend, DB, Redis, Celery)
- ✅ Un environnement de développement complet

**Prochaines étapes :**
1. Explorer l'interface utilisateur
2. Tester la création de posts
3. Consulter la documentation API : http://localhost:8000/docs
4. Configurer vos clés API (OpenAI, Stripe) dans `backend/.env`

---

**Besoin d'aide ?**
- 📖 Consultez [QUICK_START.md](QUICK_START.md)
- 🐛 Issues GitHub : https://github.com/westekey/Pyralys/issues

**Bon développement ! 🚀**
