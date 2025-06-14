#!/usr/bin/env bash
# Datei: scripts/setup-postgres.sh
# Ziel: PostgreSQL MPG erstellen & App verbinden

set -e

APP_NAME="swingmotionpro"
DB_NAME="swingmotionpro-db"
REGION="fra"

echo "🔍 Prüfe, ob MPG-Datenbank $DB_NAME existiert..."
if ! flyctl apps list | grep -q "$DB_NAME"; then
  echo "✅ Erstelle Managed Postgres $DB_NAME in Region $REGION..."
  flyctl mpg create --name "$DB_NAME" --region "$REGION"
else
  echo "ℹ️  $DB_NAME existiert bereits, überspringe Erstellung."
fi

echo "🔗 Verbinde App $APP_NAME mit Datenbank $DB_NAME..."
flyctl mpg attach "$DB_NAME" --app "$APP_NAME"

echo "🔐 Secrets in App prüfen:"
flyctl secrets list -a "$APP_NAME" | grep DATABASE_URL || echo "⚠️ Kein DATABASE_URL-Secret gefunden"

echo "✅ Managed PostgreSQL-Setup abgeschlossen."