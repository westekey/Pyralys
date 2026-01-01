#!/bin/bash

# Script de démarrage de l'environnement WordPress local Pyralys
# Ce script démarre tous les services et configure WordPress automatiquement

set -e

echo "🚀 Démarrage de l'environnement Pyralys + WordPress..."
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Installez Docker Desktop d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose n'est pas installé."
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker est installé"

# 2. Arrêter les conteneurs existants (si lancés)
echo ""
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down 2>/dev/null || true

# 3. Démarrer tous les services
echo ""
echo "🐳 Démarrage des conteneurs Docker..."
echo "   - PostgreSQL (Pyralys DB)"
echo "   - Redis (Cache)"
echo "   - Backend API (FastAPI)"
echo "   - Frontend (Next.js)"
echo "   - WordPress + MySQL"
echo "   - phpMyAdmin"
echo ""

docker-compose up -d

# 4. Attendre que les services soient prêts
echo ""
echo "⏳ Attente du démarrage des services..."
sleep 15

# 5. Vérifier que WordPress est accessible
echo ""
echo "🔍 Vérification de WordPress..."
for i in {1..30}; do
    if curl -s http://localhost:8080 > /dev/null; then
        echo -e "${GREEN}✓${NC} WordPress est accessible!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ WordPress ne démarre pas. Vérifiez les logs avec: docker-compose logs wordpress"
        exit 1
    fi
    sleep 2
done

# 6. Vérifier que l'API Pyralys est accessible
echo ""
echo "🔍 Vérification de l'API Pyralys..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✓${NC} API Pyralys est accessible!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ API Pyralys ne démarre pas. Vérifiez les logs avec: docker-compose logs backend"
        exit 1
    fi
    sleep 2
done

# 7. Afficher les informations de connexion
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🎉 Environnement Pyralys + WordPress démarré avec succès!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📍 URLs d'accès :${NC}"
echo ""
echo "  🌐 WordPress       : http://localhost:8080"
echo "  ⚙️  Admin WordPress : http://localhost:8080/wp-admin"
echo "  🚀 API Pyralys     : http://localhost:8000"
echo "  📖 API Docs        : http://localhost:8000/docs"
echo "  💻 Frontend Pyralys: http://localhost:3000"
echo "  🗄️  phpMyAdmin      : http://localhost:8081"
echo ""
echo -e "${YELLOW}🔑 Identifiants WordPress :${NC}"
echo "  Lors de la première visite, configurez :"
echo "  - Langue          : Français"
echo "  - Titre du site   : Pyralys Dev"
echo "  - Utilisateur     : admin"
echo "  - Mot de passe    : admin123"
echo "  - Email           : admin@pyralys.local"
echo ""
echo -e "${YELLOW}🔧 Configuration du plugin Pyralys :${NC}"
echo "  1. Allez sur http://localhost:8080/wp-admin"
echo "  2. Connectez-vous avec admin/admin123"
echo "  3. Allez dans Extensions > Pyralys - Activer"
echo "  4. Allez dans Pyralys AI > Settings"
echo "  5. Configurez :"
echo "     - URL API    : http://backend:8000/api/v1"
echo "     - Token API  : (obtenez-le depuis http://localhost:3000)"
echo ""
echo -e "${YELLOW}📝 Modifications en temps réel :${NC}"
echo "  - Plugin WordPress : wordpress-plugin/ (HOT-RELOAD activé)"
echo "  - Backend API      : backend/ (auto-reload avec uvicorn)"
echo "  - Frontend         : frontend/ (hot-reload Next.js)"
echo ""
echo -e "${YELLOW}🛠️  Commandes utiles :${NC}"
echo "  - Voir les logs       : docker-compose logs -f wordpress"
echo "  - Redémarrer tout     : docker-compose restart"
echo "  - Arrêter tout        : docker-compose down"
echo "  - Shell WordPress     : docker exec -it pyralys-wordpress bash"
echo "  - Shell API           : docker exec -it pyralys-backend bash"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✨ Commencez à développer!${NC}"
echo "   Modifiez vos fichiers dans wordpress-plugin/ et rechargez la page WordPress"
echo ""
