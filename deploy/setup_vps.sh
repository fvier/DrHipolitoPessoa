#!/bin/bash
# ==============================================================================
# SCRIPT DE DEPLOY AUTOMATIZADO - DR. HIPÓLITO PESSOA (VPS 147.79.110.132)
# ==============================================================================

set -e

echo "🚀 Iniciando deploy do Dr. Hipólito Pessoa no servidor 147.79.110.132..."

# 1. Cria .env.vps a partir do exemplo se não existir
if [ ! -f .env.vps ]; then
    echo "📋 Criando arquivo .env.vps a partir do .env.vps.example..."
    cp .env.vps.example .env.vps
fi

# 2. Carrega variáveis de ambiente se existirem
if [ -f .env.vps ]; then
    export $(grep -v '^#' .env.vps | xargs -d '\n' 2>/dev/null || true)
fi

# 3. Build e inicialização dos containers Docker (conectando ao coolify-proxy)
echo "📦 Construindo containers (Django + Postgres 16 + Traefik/Coolify SSL)..."
docker compose -f docker-compose.coolify.yml down || true
docker compose -f docker-compose.coolify.yml build --no-cache
docker compose -f docker-compose.coolify.yml up -d

# 4. Aguarda o container do Django iniciar
echo "⏳ Aguardando inicialização do Django e PostgreSQL..."
sleep 12

# 5. Executa criação inicial de superusuário caso não exista
echo "🌱 Verificando superusuário administrativo..."
docker compose -f docker-compose.coolify.yml exec -T app python -c '
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
from larkon.users.models import User

admin_email = os.environ.get("INITIAL_ADMIN_EMAIL", "contato@drhipolitopessoa.com.br")
admin_pass = os.environ.get("INITIAL_ADMIN_PASSWORD", "DrHipolito@2026!")

user, created = User.objects.get_or_create(
    email=admin_email,
    defaults={"name": "Dr. Hipólito Pessoa", "is_staff": True, "is_superuser": True}
)
if created and admin_pass:
    user.set_password(admin_pass)
user.is_staff = True
user.is_superuser = True
user.save()
print(f"✓ Usuário {admin_email} pronto!")
' || true

echo "=================================================================="
echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "🌐 Acesse: https://drhipolitopessoa.com.br"
echo "🔐 Admin: https://drhipolitopessoa.com.br/admin/"
echo "🔗 Links: https://drhipolitopessoa.com.br/links/"
echo "=================================================================="

