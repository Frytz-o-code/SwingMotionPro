#include .env

.PHONY: launch deploy dev proxy init-db setup-env reset-db


# 🛠 Einmaliger Launch der App auf Fly.io (ohne Deploy)
launch:
	@echo "🚀 Launching app..."
	flyctl launch --no-deploy --auto-confirm

# 📦 Deploy auf Fly.io
deploy:
	@echo "📦 Deploying app..."
	flyctl deploy

# 💻 Lokale Entwicklung starten (via uv)
dev: setup-env
	uv run -m app.app

# 🌀 Fly.io Proxy starten für lokale DB-Verbindung
proxy:
	@echo "🌀 Starte Fly Proxy für lokale DB auf Port 5432..."
	@nohup fly proxy 5432:5432 -a swingmotionpro-db > /dev/null 2>&1 &

# 🔐 .env automatisch erzeugen (aus GitHub Secrets via Codespace oder lokal)
setup-env:
	@echo "🔐 Erzeuge .env..."
	@echo "ENV=development" > .env
	@echo "DATABASE_URL=$${DATABASE_URL_DEV}" >> .env
	@echo "SECRET_KEY=$${SECRET_KEY:-dev-secret}" >> .env

# 🧱 Datenbankinitialisierung lokal (nur dev)
init-db:
	uv run scripts/init_db.py

# ⚠️ Datenbank löschen und erneut initialisieren (nur in Dev-Umgebung!)
reset-db:
	@echo "🧨 Dropping all tables in dev DB..."
	uv run scripts/drop_all.py
	@echo "🔁 Re-initialisiere Schema..."
	uv run scripts/init_db.py
