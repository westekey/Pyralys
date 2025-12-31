#!/bin/bash

# Script d'installation automatique de WordPress avec le plugin Pyralys
# Ce script configure WordPress automatiquement sans intervention manuelle

set -e

echo "🔧 Configuration automatique de WordPress + Plugin Pyralys..."
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 1. Attendre que WordPress soit prêt
echo "⏳ Attente du démarrage complet de WordPress..."
sleep 10

# 2. Installer WP-CLI dans le conteneur WordPress
echo ""
echo "📦 Installation de WP-CLI..."
docker exec pyralys-wordpress bash -c "
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
    chmod +x wp-cli.phar
    mv wp-cli.phar /usr/local/bin/wp
" 2>/dev/null || echo "WP-CLI déjà installé"

# 3. Vérifier si WordPress est déjà installé
IS_INSTALLED=$(docker exec pyralys-wordpress wp core is-installed --allow-root 2>/dev/null && echo "yes" || echo "no")

if [ "$IS_INSTALLED" = "yes" ]; then
    echo -e "${YELLOW}ℹ️  WordPress est déjà installé${NC}"
else
    # 4. Installer WordPress
    echo ""
    echo "🚀 Installation de WordPress..."
    docker exec pyralys-wordpress wp core install \
        --url="http://localhost:8080" \
        --title="Pyralys Development" \
        --admin_user="admin" \
        --admin_password="admin123" \
        --admin_email="admin@pyralys.local" \
        --skip-email \
        --allow-root

    echo -e "${GREEN}✓${NC} WordPress installé"
fi

# 5. Activer le mode débogage
echo ""
echo "🔧 Configuration du mode développement..."
docker exec pyralys-wordpress wp config set WP_DEBUG true --raw --allow-root
docker exec pyralys-wordpress wp config set WP_DEBUG_LOG true --raw --allow-root
docker exec pyralys-wordpress wp config set WP_DEBUG_DISPLAY false --raw --allow-root
docker exec pyralys-wordpress wp config set SCRIPT_DEBUG true --raw --allow-root

# 6. Vérifier si le plugin existe
PLUGIN_EXISTS=$(docker exec pyralys-wordpress wp plugin list --allow-root --format=csv | grep -c "pyralys" || echo "0")

if [ "$PLUGIN_EXISTS" -eq "0" ]; then
    echo -e "${YELLOW}⚠️  Plugin Pyralys non détecté. Assurez-vous que wordpress-plugin/ est monté correctement.${NC}"
else
    # 7. Activer le plugin Pyralys
    echo ""
    echo "🔌 Activation du plugin Pyralys..."
    docker exec pyralys-wordpress wp plugin activate pyralys --allow-root 2>/dev/null && \
        echo -e "${GREEN}✓${NC} Plugin Pyralys activé" || \
        echo -e "${YELLOW}⚠️  Plugin Pyralys déjà activé ou non présent${NC}"
fi

# 8. Installer un thème moderne
echo ""
echo "🎨 Installation d'un thème moderne..."
docker exec pyralys-wordpress wp theme install twentytwentyfour --activate --allow-root 2>/dev/null || \
    echo "Thème déjà installé"

# 9. Créer quelques posts de test
echo ""
echo "📝 Création de posts de test..."
docker exec pyralys-wordpress bash -c "
    wp post create \
        --post_title='Bienvenue sur Pyralys' \
        --post_content='<p>Pyralys est votre assistant IA pour générer du contenu social media automatiquement.</p>' \
        --post_status='publish' \
        --allow-root 2>/dev/null || true

    wp post create \
        --post_title='Test de génération AI' \
        --post_content='<p>Ce post a été créé pour tester la génération de contenu avec Pyralys AI.</p>' \
        --post_status='draft' \
        --allow-root 2>/dev/null || true
" 2>/dev/null || echo "Posts de test déjà créés"

# 10. Configuration des permaliens
echo ""
echo "🔗 Configuration des permaliens..."
docker exec pyralys-wordpress wp rewrite structure '/%postname%/' --allow-root

# 11. Créer un Application Password pour l'API
echo ""
echo "🔑 Création d'un Application Password pour Pyralys..."
APP_PASSWORD=$(docker exec pyralys-wordpress wp user application-password create admin pyralys-api --porcelain --allow-root 2>/dev/null || echo "")

if [ -n "$APP_PASSWORD" ]; then
    echo -e "${GREEN}✓${NC} Application Password créé: $APP_PASSWORD"
    echo ""
    echo "Sauvegardez ce mot de passe pour connecter Pyralys à WordPress!"
else
    echo -e "${YELLOW}ℹ️  Application Password peut être créé manuellement depuis WP Admin${NC}"
fi

# 12. Afficher le résumé
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}✅ WordPress configuré avec succès!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📍 Accédez à WordPress :${NC}"
echo "  🌐 Site       : http://localhost:8080"
echo "  ⚙️  Admin     : http://localhost:8080/wp-admin"
echo ""
echo -e "${YELLOW}🔑 Connexion WordPress :${NC}"
echo "  👤 Utilisateur: admin"
echo "  🔒 Mot de passe: admin123"
echo ""
if [ -n "$APP_PASSWORD" ]; then
    echo -e "${YELLOW}🔐 Application Password (pour API Pyralys) :${NC}"
    echo "  $APP_PASSWORD"
    echo ""
fi
echo -e "${YELLOW}🎯 Prochaines étapes :${NC}"
echo "  1. Connectez-vous à WordPress"
echo "  2. Allez dans Pyralys AI > Settings"
echo "  3. Configurez l'API URL: http://backend:8000/api/v1"
echo "  4. Obtenez votre token Pyralys depuis http://localhost:3000"
echo "  5. Testez la génération de contenu!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
