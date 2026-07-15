# mcp-russia — Makefile

.DEFAULT_GOAL := help
.PHONY: help sync dev test test-feature lint fix types run serve inspect ci clean build changelog version release-patch release-minor release-major diagrams

## —— Настройка ——

help: ## Показать справку
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

sync: ## Установить рабочие зависимости
	uv sync

dev: ## Установить все зависимости (рабочие + разработка)
	uv sync --group dev

## —— Качество ——

lint: ## Проверка линтером и форматирования
	uv run ruff check src/ tests/ && uv run ruff format --check src/ tests/

fix: ## Автоисправление линтера и форматирования
	uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/

types: ## Строгая проверка типов mypy
	uv run mypy src/mcp_russia/

test: ## Запустить все тесты
	uv run pytest -v

test-feature: ## Запустить тесты одного модуля (использование: make test-feature F=cbrf)
	uv run pytest tests/data/$(F)/ -v 2>/dev/null || uv run pytest tests/agenty/$(F)/ -v

ci: lint types test ## Полный CI-конвейер: линтер + типы + тесты

## —— Сервер ——

run: ## Запустить MCP-сервер (stdio)
	uv run python -m mcp_russia.server

serve: ## Запустить MCP-сервер (HTTP :8000)
	uv run python -c "from mcp_russia.server import mcp; mcp.run(transport='streamable-http', host='0.0.0.0', port=8000)"

inspect: ## Показать инструменты/ресурсы/промпты MCP-сервера
	uv run python -c "from mcp_russia.server import mcp, reyestr; print(reyestr.svodka())"

## —— Релиз ——

version: ## Показать текущую версию
	@uv version

build: ## Собрать пакет (sdist + wheel)
	uv build

changelog: ## Сгенерировать CHANGELOG.md с помощью git-cliff
	git cliff -o CHANGELOG.md

release-patch: ci ## Релиз патч-версии (0.1.0 → 0.1.1)
	@scripts/release.sh patch

release-minor: ci ## Релиз минорной версии (0.1.0 → 0.2.0)
	@scripts/release.sh minor

release-major: ci ## Релиз мажорной версии (0.1.0 → 1.0.0)
	@scripts/release.sh major

## —— Документация ——

diagrams: ## Сгенерировать диаграммы архитектуры (требуется graphviz)
	uv run python scripts/generate_diagrams.py

## —— Разное ——

clean: ## Удалить артефакты сборки и кеши
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
