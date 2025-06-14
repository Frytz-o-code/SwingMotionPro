#!/usr/bin/env bash
# scripts/dev_start_db_proxy.sh

echo "🚀 Starte Fly Postgres Proxy auf Port 5433 …"

if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl nicht gefunden!"
    exit 1
fi

flyctl auth token | grep -q . || {
    echo "❌ Nicht bei Fly.io angemeldet – bitte via fly auth login"
    exit 1
}

# Hintergrund-Proxy starten
flyctl proxy -a swingmotionpro-db -p 5433 > /tmp/fly-proxy.log 2>&1 &

echo "✅ Proxy läuft auf localhost:5433"