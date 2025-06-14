#!/usr/bin/env bash
# Erstellt .env aus GitHub Secrets

echo "🔧 Erzeuge lokale .env Datei …"

# ENV (default = development)
echo "ENV=${ENV:-development}" > .env

# Lokale Entwicklungsdatenbank
if [ -n "$DATABASE_URL_DEV" ]; then
  echo "DATABASE_URL_DEV=$DATABASE_URL_DEV" >> .env
  echo "✅ DATABASE_URL_DEV gesetzt."
else
  echo "⚠️  DATABASE_URL_DEV nicht gefunden – bitte in GitHub Secrets definieren."
fi

# Optionale weitere Einträge
# echo "FLY_API_TOKEN=$FLY_API_TOKEN" >> .env

echo "✅ .env erfolgreich erzeugt."