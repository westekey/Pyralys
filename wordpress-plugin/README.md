# Pyralys WordPress Plugin

Plugin WordPress pour générer du contenu AI directement depuis votre tableau de bord WordPress.

## 🚀 Fonctionnalités

- ✨ **Génération de contenu AI** : Créez des captions optimisées avec GPT-4
- 🖼️ **Génération d'images** : Intégration DALL-E 3 (future release)
- 🏷️ **Hashtags intelligents** : Suggestions automatiques de hashtags
- 📝 **Multi-plateforme** : Optimisé pour WordPress, Instagram, LinkedIn, Facebook
- 🎨 **4 tons disponibles** : Casual, Professionnel, Drôle, Inspirant

## 📦 Installation

### Option 1: Installation manuelle

1. Téléchargez le dossier `wordpress-plugin`
2. Renommez-le en `pyralys`
3. Uploadez-le dans `/wp-content/plugins/` de votre site WordPress
4. Activez le plugin depuis le menu "Extensions" de WordPress

### Option 2: Via ZIP

1. Créez un fichier ZIP du dossier `wordpress-plugin`
2. Dans WordPress, allez dans Extensions > Ajouter
3. Cliquez sur "Téléverser une extension"
4. Sélectionnez le fichier ZIP et installez

## ⚙️ Configuration

### 1. Configuration du serveur Pyralys

Assurez-vous que votre serveur Pyralys backend est en cours d'exécution :

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Configuration WordPress

1. Allez dans **Pyralys AI > Settings**
2. Configurez l'URL de l'API :
   - Pour serveur local : `http://localhost:8000/api/v1`
   - Pour serveur distant : `https://votre-domaine.com/api/v1`
3. Entrez votre token d'authentification Pyralys
4. Cliquez sur "Test Connection" pour vérifier

### 3. Obtenir votre token API

Pour obtenir votre token d'authentification :

1. Créez un compte sur Pyralys (via l'interface frontend)
2. Connectez-vous pour obtenir votre access token
3. Ou utilisez l'API directement :

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=votre@email.com&password=votrepassword"
```

## 📖 Utilisation

### Génération depuis l'éditeur de post

1. Créez un nouveau post dans WordPress
2. Dans la barre latérale, trouvez la box "Pyralys AI Generator"
3. Entrez votre prompt (ex: "Coucher de soleil à la plage")
4. Sélectionnez la plateforme et le ton
5. Cliquez sur "Generate Content"
6. Cliquez sur "Insert into Post" pour insérer le contenu

### Depuis le tableau de bord

1. Allez dans **Pyralys AI** dans le menu WordPress
2. Suivez les instructions pour commencer

## 🔧 Configuration avancée

### Application Password WordPress (pour API REST)

Pour permettre à Pyralys de publier directement sur WordPress :

1. Allez dans **Utilisateurs > Profil**
2. Descendez jusqu'à "Mots de passe d'application"
3. Créez un nouveau mot de passe d'application nommé "Pyralys"
4. Utilisez ce mot de passe dans l'interface Pyralys

### Connexion au serveur local

Si vous utilisez Pyralys en serveur local sur le même ordinateur que WordPress :

- **URL API** : `http://localhost:8000/api/v1`
- **Site WordPress** : `http://localhost/wordpress` (ou votre configuration locale)

### Configuration pour production

Pour un environnement de production :

1. Déployez le backend Pyralys sur un serveur
2. Configurez HTTPS
3. Mettez à jour l'URL dans les settings du plugin
4. Utilisez des variables d'environnement sécurisées

## 🎯 Cas d'usage

### Blogueurs WordPress

```
1. Créez un nouveau post
2. Générez du contenu AI optimisé SEO
3. Ajoutez des hashtags pertinents
4. Publiez instantanément
```

### Agences de marketing

```
1. Créez du contenu pour plusieurs clients
2. Utilisez différents tons selon la marque
3. Optimisez pour différentes plateformes
4. Programmez la publication
```

### E-commerce

```
1. Générez des descriptions de produits
2. Créez des posts pour les réseaux sociaux
3. Optimisez le contenu pour le SEO
4. Multipliez votre présence en ligne
```

## 🐛 Dépannage

### Le plugin ne se connecte pas à l'API

- Vérifiez que le serveur Pyralys est en cours d'exécution
- Vérifiez l'URL de l'API dans les settings
- Vérifiez que le token est valide
- Vérifiez les logs du serveur Pyralys

### Erreur CORS

Si vous avez des erreurs CORS, ajoutez votre domaine WordPress aux CORS origins dans `backend/app/core/config.py` :

```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",  # Ajoutez votre URL WordPress
]
```

### Le contenu ne s'insère pas

- Vérifiez que vous utilisez l'éditeur Gutenberg ou Classic Editor
- Vérifiez la console JavaScript pour les erreurs
- Essayez de copier-coller manuellement

## 📝 Changelog

### Version 1.0.0 (2025-01-01)
- 🎉 Version initiale
- ✨ Génération de captions AI
- 🏷️ Suggestions de hashtags
- ⚙️ Interface d'administration
- 🔌 Intégration éditeur WordPress

## 🤝 Support

Pour obtenir de l'aide :

1. Consultez la documentation : https://docs.pyralys.com
2. Ouvrez une issue sur GitHub
3. Contactez le support : support@pyralys.com

## 📄 Licence

GPL v2 or later

## 🔐 Sécurité

- Tous les tokens sont stockés de manière sécurisée dans la base de données WordPress
- Les communications avec l'API utilisent HTTPS en production
- Les données ne sont jamais partagées avec des tiers

## 🚀 Prochaines fonctionnalités

- [ ] Génération d'images DALL-E 3
- [ ] Publication multi-plateformes depuis WordPress
- [ ] Analytics intégrés
- [ ] Programmation de publications
- [ ] Support WooCommerce
- [ ] Templates de contenu
