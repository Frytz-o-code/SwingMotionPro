#!/usr/bin/env bash
# filepath: .devcontainer/install-uv.sh

set -e

if command -v uv >/dev/null 2>&1; then
  echo "uv ist bereits installiert."
else
  echo "uv wird installiert..."
  curl -Ls https://astral.sh/uv/install.sh | bash
  echo "uv wurde installiert."
fi