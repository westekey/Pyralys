# 📸 Instagram Integration - Guide Rapide

## Vue d'ensemble

Pyralys est maintenant intégré avec **Instagram Graph API** ! Vous pouvez :
- ✅ Connecter votre compte Instagram via OAuth 2.0
- ✅ Publier des photos avec captions et hashtags
- ✅ Publier des carrousels (2-10 images)
- ✅ Publier des stories (24h)
- ✅ Consulter les insights (engagement, reach, impressions)

## 🔑 Prérequis

### 1. Créer une application Facebook

Instagram utilise Facebook pour l'authentification OAuth. Vous devez :

1. Aller sur https://developers.facebook.com
2. Créer une application Facebook
3. Ajouter le produit "Instagram Graph API"
4. Configurer OAuth redirect URIs

### 2. Configuration

Dans `/backend/.env`, ajoutez :

```env
# Facebook/Instagram OAuth
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret

# Redirect URI (doit correspondre à la config Facebook)
INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/v1/instagram/oauth/callback
```

### 3. Type de compte requis

**Important** : Pour publier du contenu, vous avez besoin d'un compte :
- **Business Instagram** OU
- **Creator Instagram**

Les comptes personnels peuvent uniquement s'authentifier mais ne peuvent pas publier.

## 🚀 Flow OAuth - Connexion Instagram

### Étape 1 : Obtenir l'URL d'autorisation

```bash
curl -X GET http://localhost:8000/api/v1/instagram/oauth/authorize \
  -H "Authorization: Bearer YOUR_PYRALYS_TOKEN"
```

Réponse :
```json
{
  "authorization_url": "https://api.instagram.com/oauth/authorize?client_id=...",
  "message": "Redirect user to this URL"
}
```

### Étape 2 : Rediriger l'utilisateur

Redirigez l'utilisateur vers `authorization_url`. Il sera redirigé vers Instagram pour autoriser l'application.

### Étape 3 : Callback automatique

Après autorisation, Instagram redirige vers :
```
http://localhost:8000/api/v1/instagram/oauth/callback?code=XXX&state=user_XXX
```

Le backend :
1. Échange le code contre un token d'accès
2. Convertit le token court (1h) en token longue durée (60 jours)
3. Récupère les infos du profil Instagram
4. Sauvegarde le compte en base de données
5. Redirige vers le frontend avec succès

## 📤 Publication de contenu

### Publier une photo

```bash
curl -X POST http://localhost:8000/api/v1/instagram/publish/photo \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instagram_account_id": 1,
    "image_url": "https://example.com/image.jpg",
    "caption": "Check out this amazing sunset! 🌅 #sunset #nature #beautiful"
  }'
```

**Important** : L'image doit être :
- Hébergée publiquement (accessible via URL)
- Format JPEG ou PNG
- Dimensions recommandées : 1080x1080 (carré), 1080x1350 (portrait)

### Publier un carrousel (album)

```bash
curl -X POST http://localhost:8000/api/v1/instagram/publish/carousel \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instagram_account_id": 1,
    "images": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg",
      "https://example.com/image3.jpg"
    ],
    "caption": "Swipe to see more! 👉 #carousel #album"
  }'
```

Contraintes :
- Minimum : 2 images
- Maximum : 10 images
- Toutes les images doivent être du même ratio (carré, portrait, ou paysage)

### Publier une story

```bash
curl -X POST http://localhost:8000/api/v1/instagram/publish/story \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instagram_account_id": 1,
    "media_url": "https://example.com/story.jpg",
    "media_type": "IMAGE"
  }'
```

Les stories :
- Disparaissent après 24 heures
- Dimensions recommandées : 1080x1920 (9:16)
- Peuvent être des images ou des vidéos

## 📊 Analytics & Insights

### Récupérer les insights d'un post

```bash
curl -X GET "http://localhost:8000/api/v1/instagram/media/MEDIA_ID/insights?instagram_account_id=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Métriques disponibles :
- `engagement` - Likes + commentaires + saves + shares
- `impressions` - Nombre total de vues
- `reach` - Nombre d'utilisateurs uniques atteints
- `saved` - Nombre de sauvegardes

## 🔄 Gestion des comptes

### Lister les comptes connectés

```bash
curl -X GET http://localhost:8000/api/v1/instagram/accounts \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Rafraîchir un compte

```bash
curl -X POST http://localhost:8000/api/v1/instagram/accounts/1/refresh \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Ceci va :
- Prolonger le token d'accès de 60 jours
- Mettre à jour les stats du profil (followers, posts, etc.)

### Déconnecter un compte

```bash
curl -X DELETE http://localhost:8000/api/v1/instagram/accounts/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🤖 Publier du contenu AI généré

### Workflow complet

```bash
# 1. Générer du contenu AI
CAPTION=$(curl -X POST http://localhost:8000/api/v1/ai/generate-caption \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Beautiful sunset at the beach",
    "platform": "instagram",
    "tone": "casual"
  }')

# 2. Générer une image AI
IMAGE=$(curl -X POST http://localhost:8000/api/v1/ai/generate-image \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Beautiful sunset at the beach with palm trees",
    "style": "vibrant",
    "size": "1024x1024"
  }')

# 3. Publier sur Instagram
curl -X POST http://localhost:8000/api/v1/instagram/publish/photo \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"instagram_account_id\": 1,
    \"image_url\": \"$IMAGE_URL\",
    \"caption\": \"$CAPTION_TEXT\"
  }"
```

## ⚠️ Limitations & Restrictions

### Limites Instagram API

- **Rate limits** : ~200 requêtes par heure
- **Publication** : Pas de limite stricte mais évitez le spam
- **Stories** : Pas plus de 10-15 par heure recommandé
- **Token expiration** : 60 jours (rafraîchir avant expiration)

### Restrictions de contenu

Instagram refuse :
- Images < 320px
- Vidéos stories > 15 secondes
- Contenus violant les règles de la communauté
- URLs non HTTPS

### Comptes

- **Personal accounts** : Connexion OK, publication NON
- **Business accounts** : Toutes les fonctionnalités
- **Creator accounts** : Toutes les fonctionnalités

## 🔐 Sécurité

### Tokens

- Les tokens sont stockés chiffrés en base de données
- Durée de vie : 60 jours (renouvelables)
- Rafraîchir automatiquement avant expiration
- Ne jamais exposer les tokens côté client

### HTTPS requis en production

En production, vous DEVEZ :
- Utiliser HTTPS pour tous les endpoints
- Configurer un domaine vérifié dans Facebook
- Utiliser des variables d'environnement sécurisées

## 🧪 Testing

### Mode développement

1. Créez une app Facebook en mode développement
2. Ajoutez votre compte Instagram comme testeur
3. Testez avec ce compte uniquement

### Mode production

1. Soumettez l'app pour révision Facebook
2. Demandez les permissions requises :
   - `instagram_basic`
   - `instagram_content_publish`
   - `instagram_manage_insights`
3. Attendez l'approbation (1-7 jours)

## 📝 Endpoints disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/instagram/oauth/authorize` | GET | Obtenir URL d'autorisation OAuth |
| `/instagram/oauth/callback` | GET | Callback OAuth (automatique) |
| `/instagram/accounts` | GET | Lister les comptes connectés |
| `/instagram/accounts/{id}` | DELETE | Déconnecter un compte |
| `/instagram/accounts/{id}/refresh` | POST | Rafraîchir le compte et le token |
| `/instagram/publish/photo` | POST | Publier une photo |
| `/instagram/publish/carousel` | POST | Publier un carrousel |
| `/instagram/publish/story` | POST | Publier une story |
| `/instagram/media/{id}/insights` | GET | Récupérer les insights |

## 🎉 Prochaines étapes

Maintenant que l'intégration Instagram est complète, vous pouvez :

1. ✅ Connecter votre compte Instagram
2. ✅ Publier du contenu AI généré automatiquement
3. ⏳ Ajouter le scheduling (Sprint 5)
4. ⏳ Créer un dashboard d'analytics (Sprint 6)

Pour plus d'informations :
- **Documentation API** : http://localhost:8000/docs
- **Instagram Graph API** : https://developers.facebook.com/docs/instagram-api
- **Support Pyralys** : Créez une issue sur GitHub

**Bon développement ! 📸✨**
