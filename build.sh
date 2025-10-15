#!/usr/bin/env bash
# build.sh - Script executado pelo Render durante o build

set -o errexit  # Sai se houver erro

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build concluído com sucesso!"