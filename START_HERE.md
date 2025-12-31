# 🚀 Pyralys - Démarrage Rapide

Bienvenue dans Pyralys ! Votre plateforme de génération de contenu IA pour réseaux sociaux.

## ⚡ Démarrage Ultra-Rapide (3 commandes)

```bash
# 1. Démarrer tous les services (Pyralys + WordPress)
make wordpress-start

# 2. Configurer WordPress automatiquement
make wordpress-setup

# 3. Voir les URLs d'accès
make urls
```

**✅ C'est tout ! Votre environnement est prêt.**

## 🌐 Accès aux services

Après le démarrage, accédez à :

| Service | URL | Login |
|---------|-----|-------|
| **WordPress** | http://localhost:8080 | admin / admin123 |
| **WP Admin** | http://localhost:8080/wp-admin | admin / admin123 |
| **API Pyralys** | http://localhost:8000/docs | - |
| **Frontend Pyralys** | http://localhost:3000 | - |
| **phpMyAdmin** | http://localhost:8081 | wordpress / wordpress123 |

## 📖 Guides complets

- **[WordPress Local Dev](WORDPRESS_LOCAL_DEV.md)** - Guide complet du développement WordPress
- **[WordPress Quick Start](QUICK_START_WORDPRESS.md)** - Configuration et utilisation
- **[WordPress Plugin README](wordpress-plugin/README.md)** - Documentation du plugin

## 🎯 Que faire ensuite ?

### Option 1 : Développer le plugin WordPress

```bash
# Modifier le plugin en temps réel
code wordpress-plugin/

# Voir les modifications immédiatement
# Rechargez http://localhost:8080/wp-admin
```

Tous vos changements dans `wordpress-plugin/` sont **visibles instantanément** !

### Option 2 : Tester la génération AI

1. Allez sur http://localhost:8080/wp-admin
2. Connectez-vous (admin/admin123)
3. Allez dans **Pyralys AI > Settings**
4. Configurez l'API :
   - URL : `http://backend:8000/api/v1`
   - Token : (obtenez-le depuis http://localhost:3000)
5. Créez un nouveau post
6. Utilisez la meta box **"Pyralys AI Generator"**
7. Générez du contenu AI !

### Option 3 : Utiliser l'API directement

```bash
# Créer un compte
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'

# Se connecter
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"

# Copier le token et générer du contenu
curl -X POST http://localhost:8000/api/v1/ai/generate-caption \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Coucher de soleil à la plage",
    "platform": "instagram",
    "tone": "casual"
  }'
```

## 🛠️ Commandes utiles

```bash
# Voir toutes les commandes disponibles
make help

# Commandes principales
make wordpress-start    # Démarrer tous les services
make wordpress-setup    # Configurer WordPress
make down              # Arrêter tout
make logs              # Voir les logs
make urls              # Afficher les URLs

# Commandes WordPress spécifiques
make wp-shell          # Shell WordPress
make wp-plugin-status  # Statut du plugin
make wp-debug-log      # Logs de débogage
make wp-backup         # Sauvegarder WordPress
```

## 📁 Structure du projet

```
Pyralys/
├── backend/               # API FastAPI (Python)
│   ├── app/
│   │   ├── api/          # Endpoints REST
│   │   ├── models/       # Modèles de données
│   │   ├── services/     # Logique métier
│   │   └── schemas/      # Validation Pydantic
│   └── tests/            # Tests backend
│
├── frontend/             # Interface Next.js (React)
│   ├── app/              # Pages Next.js 14
│   ├── components/       # Composants React
│   └── lib/              # Utilitaires
│
├── wordpress-plugin/     # Plugin WordPress (HOT-RELOAD!)
│   ├── pyralys.php       # Plugin principal
│   ├── assets/           # CSS & JavaScript
│   │   ├── js/admin.js   # Interface plugin
│   │   └── css/admin.css # Styles
│   └── README.md         # Doc plugin
│
├── docs/                 # Documentation
├── docker-compose.yml    # Configuration Docker
├── Makefile              # Commandes pratiques
└── START_HERE.md         # Ce fichier !
```

## 🔥 Développement en temps réel

### Plugin WordPress

Modifiez n'importe quel fichier dans `wordpress-plugin/` :

```bash
# Éditer le JavaScript
nano wordpress-plugin/assets/js/admin.js

# Éditer le CSS
nano wordpress-plugin/assets/css/admin.css

# Éditer le PHP
nano wordpress-plugin/pyralys.php
```

**Rechargez la page WordPress → Changements visibles immédiatement !**

### Backend API

```bash
# Modifier un fichier dans backend/app/
nano backend/app/api/v1/endpoints/ai.py

# Le serveur redémarre automatiquement (uvicorn --reload)
# Testez immédiatement : http://localhost:8000/docs
```

### Frontend

```bash
# Modifier une page
nano frontend/app/page.tsx

# Next.js hot-reload automatique
# Ouvrez http://localhost:3000
```

## 🐛 Débogage

### Voir les logs

```bash
# Tous les logs
make logs

# Logs WordPress uniquement
make wordpress-logs

# Logs API uniquement
make api-logs

# Logs de débogage WordPress
make wp-debug-log
```

### Shell dans les conteneurs

```bash
# Shell WordPress
make wp-shell

# Shell API
make backend-shell

# Shell Frontend
make frontend-shell

# Shell base de données
make db-shell
```

## 🔐 Configuration de production

Pour déployer en production :

1. **Changez TOUS les mots de passe**
2. **Configurez les variables d'environnement** (.env)
3. **Utilisez HTTPS**
4. **Activez les authentifications 2FA**
5. **Limitez les accès à l'API**

⚠️ Les credentials par défaut sont **UNIQUEMENT pour le développement** !

## 📊 État du projet

✅ **Sprint 1** - Authentification (100%)
✅ **Sprint 2** - AI Generation (100%)
✅ **WordPress** - Intégration complète (100%)
⏳ **Sprint 3** - Instagram OAuth (0%)
⏳ **Sprint 4** - Gestion de contenu (0%)
⏳ **Sprint 5** - Publication & Scheduling (0%)

## 🎓 Documentation complète

- **[Plan de développement MVP](docs/04-PLAN-DEVELOPPEMENT-MVP.md)**
- **[Architecture technique](docs/01-ARCHITECTURE-TECHNIQUE.md)**
- **[Spécifications fonctionnelles](docs/02-SPECIFICATIONS-FONCTIONNELLES.md)**
- **[WordPress Local Dev](WORDPRESS_LOCAL_DEV.md)**
- **[WordPress Quick Start](QUICK_START_WORDPRESS.md)**

## 🚨 Problèmes courants

### Docker ne démarre pas

```bash
# Vérifier Docker
docker --version
docker-compose --version

# Redémarrer Docker Desktop
# Puis relancer
make wordpress-start
```

### WordPress ne s'affiche pas

```bash
# Vérifier les logs
make wordpress-logs

# Reconstruire les conteneurs
make down
make wordpress-start
```

### Plugin non détecté

```bash
# Vérifier le montage du volume
docker exec pyralys-wordpress ls -la /var/www/html/wp-content/plugins/

# Si pyralys n'apparaît pas :
make down
make wordpress-start
```

### API ne répond pas

```bash
# Vérifier l'API
curl http://localhost:8000/health

# Voir les logs
make api-logs

# Redémarrer l'API
docker-compose restart backend
```

## 🎉 Prêt à commencer !

Vous êtes maintenant prêt à développer avec Pyralys !

Choisissez votre aventure :

1. 🔌 **Développer le plugin WordPress** → `code wordpress-plugin/`
2. 🚀 **Améliorer l'API** → `code backend/`
3. 💻 **Créer l'interface** → `code frontend/`
4. 📱 **Ajouter Instagram** → Sprint 3 (à venir)

**Bon développement ! 🚀**

---

**Questions ?** Consultez la documentation ou créez une issue sur GitHub.
