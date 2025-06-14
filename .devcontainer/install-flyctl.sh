#!/usr/bin/env bash
# filepath: .devcontainer/install-flyctl.sh

set -e

if command -v flyctl >/dev/null 2>&1; then
  echo "✅ flyctl ist bereits installiert: $(flyctl version)"
else
  echo "⬇️  flyctl wird installiert..."
  FLYCTL_VERSION=$(curl -s https://api.github.com/repos/superfly/flyctl/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
  curl -L "https://github.com/superfly/flyctl/releases/download/${FLYCTL_VERSION}/flyctl_${FLYCTL_VERSION#v}_linux_x86_64.tar.gz" -o flyctl.tar.gz
  tar -xzf flyctl.tar.gz
  chmod +x flyctl
  mkdir -p ~/.fly/bin
  mv flyctl ~/.fly/bin/
  rm flyctl.tar.gz
  echo 'export PATH="$HOME/.fly/bin:$PATH"' >> ~/.bashrc
  export PATH="$HOME/.fly/bin:$PATH"
  echo "✅ flyctl wurde installiert: $(flyctl version)"
fi