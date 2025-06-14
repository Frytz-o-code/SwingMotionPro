include .env

.PHONY: launch deploy

launch:
	@echo "🚀 Launching app..."
	#FLY_API_TOKEN=$(FLY_API_TOKEN) flyctl launch --no-deploy --auto-confirm
	flyctl launch --no-deploy --auto-confirm

deploy:
	@echo "📦 Deploying app..."
	#FLY_API_TOKEN=$(FLY_API_TOKEN) flyctl deploy
	flyctl deploy