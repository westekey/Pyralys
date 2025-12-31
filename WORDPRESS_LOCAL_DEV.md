# 🚀 Développement Local WordPress + Pyralys

Ce guide explique comment développer le plugin Pyralys WordPress en local avec **hot-reload** (modifications en temps réel).

## 📋 Prérequis

- Docker Desktop installé
- Docker Compose installé
- 8 GB RAM minimum
- Ports disponibles : 3000, 8000, 8080, 8081, 5432, 6379

## ⚡ Démarrage Rapide (2 commandes)

```bash
# 1. Démarrer tous les services
chmod +x start-wordpress-dev.sh
./start-wordpress-dev.sh

# 2. Configurer WordPress automatiquement
chmod +x setup-wordpress.sh
./setup-wordpress.sh
```

**C'est tout !** WordPress est maintenant configuré avec le plugin Pyralys activé.

## 🌐 URLs d'accès

| Service | URL | Description |
|---------|-----|-------------|
| WordPress | http://localhost:8080 | Site WordPress |
| WP Admin | http://localhost:8080/wp-admin | Administration WordPress |
| API Pyralys | http://localhost:8000 | Backend FastAPI |
| API Docs | http://localhost:8000/docs | Documentation interactive |
| Frontend Pyralys | http://localhost:3000 | Interface Next.js |
| phpMyAdmin | http://localhost:8081 | Gestion base de données |

## 🔑 Identifiants par défaut

### WordPress
- **Utilisateur** : admin
- **Mot de passe** : admin123
- **Email** : admin@pyralys.local

### Base de données WordPress
- **Host** : localhost:3307
- **Database** : wordpress
- **User** : wordpress
- **Password** : wordpress123

### phpMyAdmin
- **Server** : wordpress_mysql
- **Username** : wordpress
- **Password** : wordpress123

## 🔧 Structure des fichiers

```
Pyralys/
├── wordpress-plugin/          ← Votre code plugin (HOT-RELOAD)
│   ├── pyralys.php            ← Plugin principal
│   ├── assets/
│   │   ├── js/admin.js        ← JavaScript (modifiable en temps réel)
│   │   └── css/admin.css      ← CSS (modifiable en temps réel)
│   ├── README.md
│   └── INSTALLATION.md
├── backend/                   ← API Pyralys (auto-reload)
├── frontend/                  ← Interface Pyralys (hot-reload)
└── docker-compose.yml         ← Configuration Docker
```

## ✨ Hot-Reload : Modifier le plugin en temps réel

### Comment ça marche ?

Le dossier `wordpress-plugin/` est **monté directement** dans le conteneur WordPress.

Cela signifie que :
- ✅ Toute modification de fichier est **immédiatement visible**
- ✅ Pas besoin de reconstruire Docker
- ✅ Pas besoin de redémarrer WordPress
- ✅ Rechargez simplement la page !

### Exemples de modifications

#### 1. Modifier le JavaScript

```bash
# Éditez wordpress-plugin/assets/js/admin.js
nano wordpress-plugin/assets/js/admin.js

# Modifiez par exemple le message de succès
// Ancienne ligne 54 :
alert('Content inserted successfully!');

// Nouvelle ligne :
alert('✨ Contenu inséré avec succès!');

# Sauvegardez et rechargez WordPress → changement visible immédiatement!
```

#### 2. Modifier le CSS

```bash
# Éditez wordpress-plugin/assets/css/admin.css
nano wordpress-plugin/assets/css/admin.css

# Ajoutez un style personnalisé
.pyralys-tag {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 6px 12px;
    border-radius: 20px;
}

# Rechargez → nouveau style appliqué!
```

#### 3. Modifier le PHP (nécessite un rechargement de page)

```bash
# Éditez wordpress-plugin/pyralys.php
nano wordpress-plugin/pyralys.php

# Modifiez par exemple le nom du menu
// Ligne 85 :
__('Pyralys AI', 'pyralys'),

// Devient :
__('🚀 Pyralys IA', 'pyralys'),

# Rechargez la page WP Admin → changement visible!
```

### Voir les modifications en temps réel

```bash
# Ouvrez deux terminaux :

# Terminal 1 : Voir les logs WordPress
docker-compose logs -f wordpress

# Terminal 2 : Modifier vos fichiers
code wordpress-plugin/

# Les erreurs PHP apparaîtront dans Terminal 1
```

## 🐛 Débogage

### Activer les logs WordPress

Les logs sont **déjà activés** par défaut dans `wp-config.php` :

```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

### Voir les logs

```bash
# Logs WordPress (erreurs PHP)
docker exec pyralys-wordpress tail -f /var/www/html/wp-content/debug.log

# Logs Apache (requêtes HTTP)
docker-compose logs -f wordpress

# Logs API Pyralys
docker-compose logs -f backend
```

### Erreurs courantes

#### 1. Plugin ne s'active pas

```bash
# Vérifier que le plugin est bien monté
docker exec pyralys-wordpress ls -la /var/www/html/wp-content/plugins/

# Si pyralys n'apparaît pas, relancer Docker
docker-compose down
docker-compose up -d
```

#### 2. JavaScript ne fonctionne pas

```bash
# Vider le cache du navigateur (Ctrl+Shift+R)
# Vérifier la console JavaScript (F12)

# Vérifier que le fichier est bien chargé
docker exec pyralys-wordpress ls -la /var/www/html/wp-content/plugins/pyralys/assets/js/
```

#### 3. CSS ne s'applique pas

```bash
# Forcer le rechargement CSS
# Ctrl+F5 (Windows/Linux) ou Cmd+Shift+R (Mac)

# Vider le cache WordPress
docker exec pyralys-wordpress wp cache flush --allow-root
```

## 🔄 Workflow de développement

### 1. Modifier le code

```bash
# Ouvrez votre éditeur favori
code wordpress-plugin/

# Modifiez pyralys.php, admin.js, admin.css, etc.
```

### 2. Tester immédiatement

```bash
# Rechargez WordPress dans votre navigateur
# http://localhost:8080/wp-admin

# Testez votre modification
```

### 3. Voir les erreurs

```bash
# Terminal 1 : Logs WordPress
docker-compose logs -f wordpress

# Terminal 2 : Logs debug WordPress
docker exec -it pyralys-wordpress tail -f /var/www/html/wp-content/debug.log
```

### 4. Itérer

```
Modifier code → Recharger page → Voir résultat → Répéter
```

## 🛠️ Commandes utiles

### Gestion Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Redémarrer WordPress uniquement
docker-compose restart wordpress

# Voir les logs
docker-compose logs -f wordpress

# Shell dans WordPress
docker exec -it pyralys-wordpress bash

# Shell dans l'API
docker exec -it pyralys-backend bash
```

### WordPress CLI

```bash
# Lister les plugins
docker exec pyralys-wordpress wp plugin list --allow-root

# Activer le plugin
docker exec pyralys-wordpress wp plugin activate pyralys --allow-root

# Désactiver le plugin
docker exec pyralys-wordpress wp plugin deactivate pyralys --allow-root

# Créer un post de test
docker exec pyralys-wordpress wp post create \
    --post_title='Test AI' \
    --post_status='draft' \
    --allow-root

# Lister les posts
docker exec pyralys-wordpress wp post list --allow-root

# Voir les options
docker exec pyralys-wordpress wp option list --allow-root

# Vider le cache
docker exec pyralys-wordpress wp cache flush --allow-root
```

### Base de données

```bash
# Backup de la base WordPress
docker exec pyralys-wordpress-mysql mysqldump \
    -u wordpress -pwordpress123 wordpress > backup.sql

# Restaurer la base
docker exec -i pyralys-wordpress-mysql mysql \
    -u wordpress -pwordpress123 wordpress < backup.sql

# Accès SQL direct
docker exec -it pyralys-wordpress-mysql mysql \
    -u wordpress -pwordpress123 wordpress
```

## 📊 Workflow de test

### Test du plugin

```bash
# 1. Créer un nouveau post
# http://localhost:8080/wp-admin/post-new.php

# 2. Trouver la meta box "Pyralys AI Generator"

# 3. Entrer un prompt
# Exemple : "Article sur l'IA en 2025"

# 4. Sélectionner plateforme et ton

# 5. Cliquer "Generate Content"

# 6. Vérifier le résultat dans la console (F12)

# 7. Cliquer "Insert into Post"

# 8. Vérifier que le contenu est inséré
```

### Test de l'API

```bash
# Générer un token Pyralys
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass"

# Tester la génération de caption
curl -X POST http://localhost:8000/api/v1/ai/generate-caption \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test de génération",
    "platform": "wordpress",
    "tone": "professional"
  }'
```

## 🚀 Déployer les modifications

Une fois satisfait de vos modifications :

```bash
# 1. Committer les changements
git add wordpress-plugin/
git commit -m "✨ Amélioration du plugin WordPress"
git push

# 2. Le plugin est prêt à être distribué
cd wordpress-plugin
zip -r pyralys.zip .
# Uploadez pyralys.zip sur un site WordPress de production
```

## 📦 Distribuer le plugin

### Créer un ZIP pour distribution

```bash
cd wordpress-plugin
zip -r ../pyralys-plugin-v1.0.0.zip . \
    -x "*.git*" \
    -x "node_modules/*" \
    -x "*.DS_Store"
```

### Installer sur un autre WordPress

```bash
# 1. Allez sur le WordPress cible
# 2. Extensions > Ajouter > Téléverser
# 3. Sélectionnez pyralys-plugin-v1.0.0.zip
# 4. Activez le plugin
# 5. Configurez dans Pyralys AI > Settings
```

## 🔐 Sécurité en développement

⚠️ **IMPORTANT** : Les credentials par défaut sont pour le développement UNIQUEMENT.

En production :
- Changez tous les mots de passe
- Utilisez HTTPS
- Activez les authentifications 2FA
- Limitez les accès à l'API
- Utilisez des variables d'environnement sécurisées

## 💡 Astuces

### Développement parallèle

```bash
# Terminal 1 : WordPress logs
docker-compose logs -f wordpress

# Terminal 2 : API logs
docker-compose logs -f backend

# Terminal 3 : Frontend logs
docker-compose logs -f frontend

# Terminal 4 : Votre éditeur
code .
```

### Rechargement rapide

```bash
# Plugin modifié : Ctrl+R (recharger page)
# CSS modifié    : Ctrl+Shift+R (recharger sans cache)
# PHP modifié    : Ctrl+R
# JS modifié     : Ctrl+Shift+R
```

### Snapshot de développement

```bash
# Sauvegarder l'état actuel
docker-compose stop
docker commit pyralys-wordpress pyralys-wordpress:snapshot
docker commit pyralys-wordpress-mysql pyralys-mysql:snapshot

# Restaurer si besoin
docker-compose down
docker run -d --name pyralys-wordpress pyralys-wordpress:snapshot
```

## 🎉 Prêt à développer !

Votre environnement est maintenant configuré pour le développement WordPress + Pyralys avec hot-reload complet.

Modifiez vos fichiers et voyez les changements instantanément ! 🚀

---

**Questions ?** Consultez `wordpress-plugin/README.md` ou `QUICK_START_WORDPRESS.md`
