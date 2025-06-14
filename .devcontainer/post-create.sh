#!/usr/bin/env bash
set -e

echo "🔧 Installiere flyctl..."
bash .devcontainer/install-flyctl.sh

echo "🔧 Installiere uv..."
bash .devcontainer/install-uv.sh

echo "🔧 Initialisiere Umgebung..."
bash .devcontainer/init_env.sh