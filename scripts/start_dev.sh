#!/usr/bin/env bash
set -e

# Fly Proxy starten (falls nicht läuft)
if ! pgrep -f "fly proxy 5432:5432" > /dev/null; then
  echo "📦 Starte lokalen Fly-Proxy für DB …"
  nohup fly proxy 5432:5432 -a swingmotionpro-db > /dev/null 2>&1 &
  echo "✅ Proxy läuft auf localhost:5432"
fi

# .env-Datei schreiben
echo "📝 Erzeuge .env-Datei"
cat <<EOF > .env
ENV=development
DATABASE_URL_DEV=postgresql://<user>:<pass>@localhost:5432/<dbname>
SECRET_KEY=dev-secret-key
EOF

echo "🚀 Starte App via uv"
uv run -m app.app