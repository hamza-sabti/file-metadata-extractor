.PHONY: help build run stop clean test local-install local-run

# Default target
help:
	@echo "File Metadata Extractor - Available Commands:"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  build          - Build Docker image"
	@echo "  run            - Run with Docker Compose"
	@echo "  run-prod       - Run with production profile (nginx)"
	@echo "  stop           - Stop all containers"
	@echo "  clean          - Remove containers and images"
	@echo "  logs           - View application logs"
	@echo ""
	@echo "🔧 Local Development:"
	@echo "  local-install  - Install dependencies locally"
	@echo "  local-run      - Run application locally"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test           - Run test suite"
	@echo ""
	@echo "📦 Utility:"
	@echo "  status         - Check container status"

# Docker commands
build:
	docker-compose build

run:
	docker-compose up -d

run-prod:
	docker-compose --profile production up -d

stop:
	docker-compose down

clean:
	docker-compose down --rmi all --volumes --remove-orphans

logs:
	docker-compose logs -f file-metadata-extractor

status:
	docker-compose ps

# Local development
local-install:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

local-run:
	python app.py

# Testing
test:
	python test_app.py

# Quick start
quick-start: build run
	@echo "🚀 Application started!"
	@echo "📱 Web interface: http://localhost:5000"
	@echo "🔍 Health check: http://localhost:5000/api/health"
	@echo "📋 Run 'make logs' to view logs" 