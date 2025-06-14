#!/usr/bin/env bash
# .devcontainer/install-flyctl.sh

set -e

INSTALL_DIR="/usr/local/bin"
FLYCTL_BIN="$INSTALL_DIR/flyctl"

if command -v flyctl >/dev/null 2>&1; then
  echo "✅ flyctl ist bereits installiert: $(flyctl version)"
else
  echo "⬇️  flyctl wird installiert..."
  FLYCTL_VERSION=$(curl -s https://api.github.com/repos/superfly/flyctl/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
  curl -L "https://github.com/superfly/flyctl/releases/download/${FLYCTL_VERSION}/flyctl_${FLYCTL_VERSION#v}_linux_x86_64.tar.gz" -o flyctl.tar.gz
  tar -xzf flyctl.tar.gz
  chmod +x flyctl
  sudo mv flyctl "$FLYCTL_BIN"
  rm flyctl.tar.gz
  echo "✅ flyctl wurde installiert: $($FLYCTL_BIN version)"
fi