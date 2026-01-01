# 🚀 Guide de démarrage rapide - Pyralys avec WordPress

## Vue d'ensemble

Pyralys est maintenant **entièrement compatible avec WordPress** ! Vous pouvez :

1. ✨ **Générer du contenu AI** directement depuis WordPress
2. 📤 **Publier vers WordPress** depuis l'interface Pyralys
3. 🔌 **Utiliser le plugin WordPress** pour une intégration native
4. 🌐 **Gérer plusieurs sites WordPress** depuis un seul compte Pyralys

## 🎯 Deux méthodes d'utilisation

### Méthode 1: Plugin WordPress (Recommandé pour les utilisateurs WordPress)

**Avantages** :
- Interface native dans WordPress
- Génération AI directement depuis l'éditeur
- Pas besoin de changer d'onglet

**Installation** :
```bash
# 1. Démarrer le backend Pyralys
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Copier le plugin WordPress
cp -r wordpress-plugin /chemin/vers/wordpress/wp-content/plugins/pyralys

# 3. Activer le plugin dans WordPress
# Aller dans Extensions > Pyralys - Activer
```

**Configuration** :
1. WordPress Admin > **Pyralys AI > Settings**
2. URL API : `http://localhost:8000/api/v1`
3. Token API : (obtenu après connexion Pyralys)
4. Test Connection

**Utilisation** :
1. Créer un nouveau post WordPress
2. Trouver "Pyralys AI Generator" dans la barre latérale
3. Entrer votre prompt
4. Generate > Insert into Post

📖 **Documentation complète** : `wordpress-plugin/README.md`

---

### Méthode 2: API Pyralys (Recommandé pour l'automatisation)

**Avantages** :
- Publication automatisée
- Gestion multi-sites
- Intégration avec d'autres plateformes (Instagram, LinkedIn)
- Scheduling et analytics

**Configuration WordPress** :
1. WordPress > **Utilisateurs > Profil**
2. Créer un "Application Password" nommé "Pyralys"
3. Copier le mot de passe généré

**Connexion du site WordPress à Pyralys** :

```bash
curl -X POST http://localhost:8000/api/v1/wordpress/accounts \
  -H "Authorization: Bearer YOUR_PYRALYS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "site_url": "http://localhost/wordpress",
    "username": "admin",
    "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx",
    "site_name": "Mon Blog"
  }'
```

**Publication depuis Pyralys** :

```bash
# 1. Générer du contenu AI
curl -X POST http://localhost:8000/api/v1/ai/generate-caption \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Article sur les tendances tech 2025",
    "platform": "wordpress",
    "tone": "professional"
  }'

# 2. Publier vers WordPress
curl -X POST http://localhost:8000/api/v1/wordpress/publish \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "wordpress_account_id": 1,
    "title": "Tendances Tech 2025",
    "content": "Le contenu généré...",
    "status": "draft",
    "tags": ["tech", "innovation", "2025"]
  }'
```

## 🏗️ Architecture

```
┌─────────────────────┐
│   WordPress Site    │
│                     │
│  ┌──────────────┐   │      ┌──────────────────┐
│  │ Plugin UI    │◄──┼──────┤  Pyralys Backend │
│  └──────────────┘   │      │  (FastAPI)       │
│                     │      │                  │
│  ┌──────────────┐   │      │  ┌────────────┐  │
│  │ WP REST API  │◄──┼──────┤  │ GPT-4      │  │
│  └──────────────┘   │      │  │ DALL-E 3   │  │
└─────────────────────┘      │  └────────────┘  │
                             └──────────────────┘
```

## 📦 Endpoints API disponibles

### Gestion des comptes WordPress

```bash
# Lister les comptes connectés
GET /api/v1/wordpress/accounts

# Ajouter un site WordPress
POST /api/v1/wordpress/accounts

# Tester la connexion
POST /api/v1/wordpress/accounts/{id}/test

# Supprimer un compte
DELETE /api/v1/wordpress/accounts/{id}
```

### Publication

```bash
# Publier du contenu
POST /api/v1/wordpress/publish

# Récupérer les catégories
GET /api/v1/wordpress/accounts/{id}/categories

# Récupérer les tags
GET /api/v1/wordpress/accounts/{id}/tags
```

### Génération AI

```bash
# Générer une caption
POST /api/v1/ai/generate-caption

# Générer une image
POST /api/v1/ai/generate-image

# Générer des hashtags
POST /api/v1/ai/generate-hashtags

# Consulter les quotas
GET /api/v1/ai/quotas
```

## 🔐 Sécurité

### Application Password WordPress

WordPress Application Passwords est une méthode sécurisée pour :
- ✅ Authentification sans exposer le mot de passe principal
- ✅ Révocation facile (sans changer le mot de passe principal)
- ✅ Suivi des applications connectées
- ✅ Permissions granulaires

**Création** :
1. WordPress Admin > Utilisateurs > Profil
2. Section "Application Passwords"
3. Nom : "Pyralys"
4. "Add New Application Password"

### Stockage des credentials

- ❌ Ne jamais commit les tokens dans Git
- ✅ Utiliser des variables d'environnement (.env)
- ✅ Chiffrer les Application Passwords en base
- ✅ Utiliser HTTPS en production

## 🌟 Cas d'usage

### 1. Blog WordPress avec génération AI

```python
# Scénario : Générer un article de blog complet
import requests

# 1. Générer le contenu
response = requests.post(
    "http://localhost:8000/api/v1/ai/generate-caption",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "prompt": "Guide complet sur le SEO en 2025",
        "platform": "wordpress",
        "tone": "professional"
    }
)
content = response.json()

# 2. Publier sur WordPress
response = requests.post(
    "http://localhost:8000/api/v1/wordpress/publish",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "wordpress_account_id": 1,
        "title": "SEO en 2025 : Le Guide Complet",
        "content": content["caption"],
        "status": "publish",
        "tags": content["hashtags"]
    }
)

print(f"Article publié : {response.json()['post_url']}")
```

### 2. Publication multi-plateformes

```python
# Scénario : Un contenu, plusieurs plateformes
content = generate_ai_content("Lancement nouveau produit")

# WordPress
publish_to_wordpress(content)

# Instagram
publish_to_instagram(content)

# LinkedIn
publish_to_linkedin(content)
```

### 3. Automation avec scheduling

```python
# Scénario : Publication programmée quotidienne
import schedule
import time

def daily_blog_post():
    # Générer contenu
    content = generate_ai_content(
        prompt="Astuce du jour pour entrepreneurs",
        tone="inspirational"
    )

    # Publier sur WordPress
    publish_to_wordpress(
        title=f"Astuce du {datetime.now().strftime('%d/%m/%Y')}",
        content=content["caption"],
        status="publish"
    )

# Exécuter tous les jours à 9h
schedule.every().day.at("09:00").do(daily_blog_post)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🧪 Test de l'intégration

### Test rapide du plugin

```bash
# 1. Démarrer Pyralys backend
cd backend
python -m uvicorn app.main:app --reload

# 2. Démarrer WordPress (XAMPP/MAMP/Local)
# Ouvrir http://localhost/wordpress

# 3. Installer et activer le plugin
# Extensions > Ajouter > Téléverser pyralys.zip

# 4. Configurer
# Pyralys AI > Settings > Test Connection

# 5. Tester
# Posts > Ajouter > Pyralys AI Generator
```

### Test de l'API

```bash
# 1. Obtenir un token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass" \
  | jq -r '.access_token')

# 2. Connecter WordPress
curl -X POST http://localhost:8000/api/v1/wordpress/accounts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "site_url": "http://localhost/wordpress",
    "username": "admin",
    "app_password": "YOUR_APP_PASSWORD"
  }'

# 3. Tester la connexion
curl http://localhost:8000/api/v1/wordpress/accounts \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 Quotas et limites

Les quotas s'appliquent aussi pour WordPress :

| Plan | Captions/mois | Images/mois | Publications |
|------|--------------|-------------|--------------|
| Free | 10 | 0 | 5 |
| Premium | 100 | 50 | 50 |
| Pro | Illimité | 200 | Illimité |

## 🐛 Dépannage

### Le plugin ne se connecte pas

```bash
# Vérifier que le serveur est actif
curl http://localhost:8000/health

# Vérifier les CORS
# Dans backend/app/core/config.py, ajouter :
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8000"
]
```

### Erreur d'authentification WordPress

```bash
# Vérifier l'Application Password
curl -X GET http://localhost/wordpress/wp-json/wp/v2/posts \
  -u "username:xxxx xxxx xxxx xxxx xxxx xxxx"

# Si ça fonctionne, le problème vient de Pyralys
# Si ça ne fonctionne pas, recréer l'Application Password
```

### Publication échoue

```bash
# Vérifier les permissions WordPress
# L'utilisateur doit avoir le rôle "Editor" ou "Administrator"

# Vérifier les logs Pyralys
tail -f backend/logs/app.log
```

## 📚 Ressources

- **Documentation Plugin** : `wordpress-plugin/README.md`
- **Guide Installation** : `wordpress-plugin/INSTALLATION.md`
- **API Documentation** : http://localhost:8000/docs
- **WordPress REST API** : https://developer.wordpress.org/rest-api/

## 🎉 Prochaines étapes

Maintenant que WordPress est intégré, vous pouvez :

1. ✅ Générer du contenu AI pour WordPress
2. ✅ Publier automatiquement
3. ⏳ Ajouter Instagram (Sprint 3)
4. ⏳ Ajouter le scheduling (Sprint 5)
5. ⏳ Ajouter les analytics (Sprint 6)

**Bon développement avec Pyralys + WordPress ! 🚀**
