# Guide d'installation rapide - Pyralys WordPress Plugin

## 🎯 Installation en 5 minutes

### Prérequis

- WordPress 5.8 ou supérieur
- PHP 7.4 ou supérieur
- Serveur Pyralys backend en cours d'exécution

### Étape 1: Démarrer le serveur Pyralys

```bash
# Depuis le dossier racine de Pyralys
cd backend

# Installer les dépendances (si ce n'est pas déjà fait)
pip install -r requirements.txt

# Démarrer le serveur
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur devrait maintenant être accessible sur `http://localhost:8000`

### Étape 2: Installer le plugin WordPress

#### Option A: Installation manuelle

1. Copiez le dossier `wordpress-plugin`
2. Renommez-le en `pyralys`
3. Placez-le dans `/wp-content/plugins/` de votre installation WordPress

```bash
# Depuis le dossier racine de Pyralys
cp -r wordpress-plugin /chemin/vers/wordpress/wp-content/plugins/pyralys
```

#### Option B: Via l'interface WordPress

1. Créez un ZIP du dossier :
```bash
cd wordpress-plugin
zip -r pyralys.zip .
```

2. Dans WordPress :
   - Allez dans **Extensions > Ajouter**
   - Cliquez sur **Téléverser une extension**
   - Sélectionnez `pyralys.zip`
   - Cliquez sur **Installer maintenant**

### Étape 3: Activer le plugin

1. Dans WordPress, allez dans **Extensions**
2. Trouvez "Pyralys - AI Content Generator"
3. Cliquez sur **Activer**

### Étape 4: Configuration

1. Allez dans **Pyralys AI > Settings**
2. Configurez les paramètres :

   **URL de l'API** : `http://localhost:8000/api/v1`

   **Token API** : Obtenez-le en vous connectant à Pyralys

3. Cliquez sur **Save Settings**
4. Cliquez sur **Test Connection** pour vérifier

### Étape 5: Obtenir votre token API

#### Méthode 1: Via l'interface Pyralys

1. Ouvrez `http://localhost:3000` (frontend Pyralys)
2. Connectez-vous avec votre compte
3. Le token sera visible dans les DevTools (Network tab)

#### Méthode 2: Via API

```bash
# Créer un compte
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "votre@email.com",
    "password": "votrepassword",
    "full_name": "Votre Nom"
  }'

# Se connecter (récupérer le token)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=votre@email.com&password=votrepassword"
```

Copiez le `access_token` de la réponse.

## ✅ Vérification de l'installation

### Test 1: Page d'accueil

1. Allez dans **Pyralys AI** dans le menu WordPress
2. Vous devriez voir la page d'accueil du plugin

### Test 2: Connexion API

1. Allez dans **Pyralys AI > Settings**
2. Cliquez sur **Test Connection**
3. Vous devriez voir "✓ Connection successful!"

### Test 3: Génération de contenu

1. Créez un nouveau post WordPress
2. Dans la barre latérale, trouvez "Pyralys AI Generator"
3. Entrez un prompt : "Article sur l'intelligence artificielle"
4. Sélectionnez Plateforme: WordPress, Tone: Professional
5. Cliquez sur "Generate Content"
6. Le contenu devrait apparaître en quelques secondes

## 🔧 Configuration serveur local WordPress

### XAMPP

Si vous utilisez XAMPP :

```
URL WordPress: http://localhost/wordpress
URL API Pyralys: http://localhost:8000/api/v1
```

### MAMP

Si vous utilisez MAMP :

```
URL WordPress: http://localhost:8888
URL API Pyralys: http://localhost:8000/api/v1
```

### Local by Flywheel

Si vous utilisez Local :

```
URL WordPress: http://monsite.local
URL API Pyralys: http://localhost:8000/api/v1
```

## 🌐 Configuration pour serveur distant

Si votre WordPress est hébergé en ligne :

1. Déployez le backend Pyralys sur un serveur (Heroku, DigitalOcean, etc.)
2. Configurez HTTPS
3. Dans les settings du plugin, utilisez :
   ```
   URL API: https://api.pyralys.com/api/v1
   ```

### Configuration CORS

Ajoutez votre domaine WordPress dans `backend/app/core/config.py` :

```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",
    "https://votre-site-wordpress.com",  # Ajoutez votre domaine
]
```

Redémarrez le serveur Pyralys après modification.

## 🐛 Résolution des problèmes courants

### Erreur: "Could not connect to API server"

**Solution** :
1. Vérifiez que le serveur Pyralys est démarré
2. Vérifiez l'URL de l'API dans les settings
3. Vérifiez les logs du serveur : `http://localhost:8000/docs`

### Erreur: "Authentication failed"

**Solution** :
1. Vérifiez que votre token est correct
2. Reconnectez-vous pour obtenir un nouveau token
3. Vérifiez que le token n'a pas expiré

### Erreur CORS

**Solution** :
1. Ajoutez votre domaine WordPress dans `CORS_ORIGINS`
2. Redémarrez le serveur Pyralys
3. Videz le cache du navigateur

### Le contenu ne s'insère pas

**Solution** :
1. Vérifiez que vous utilisez Gutenberg ou Classic Editor
2. Essayez de copier-coller manuellement le contenu
3. Vérifiez la console JavaScript (F12) pour les erreurs

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs du serveur Pyralys
2. Vérifiez la console JavaScript de WordPress
3. Consultez la documentation complète : `wordpress-plugin/README.md`
4. Ouvrez une issue sur GitHub

## ✨ Prêt à utiliser !

Votre installation est maintenant complète !

Créez votre premier post avec l'IA en allant dans :
**Posts > Ajouter**

Bonne création de contenu ! 🚀
