.DEFAULT_GOAL := help

NODE := npm
POETRY := poetry

.PHONY: help install install-node install-python dev tailwind tailwind-build graph format

help:
	@printf "Targets:\n"
	@printf "  install         Install Node and Python dependencies\n"
	@printf "  install-node    npm install\n"
	@printf "  install-python  poetry install\n"
	@printf "  dev             Run the live server\n"
	@printf "  tailwind        Watch and rebuild Tailwind CSS\n"
	@printf "  tailwind-build  Build minified Tailwind CSS\n"
	@printf "  graph           Generate static/garden_map.html\n"
	@printf "  format          Run Prettier on source HTML/CSS\n"

install: install-node install-python

install-node:
	$(NODE) install

install-python:
	$(POETRY) install

dev:
	$(NODE) run server

tailwind:
	$(NODE) run tailwind

tailwind-build:
	$(NODE) run tailwind:build

graph:
	$(POETRY) run python knowledge_graph.py .

format:
	npx prettier --write "index.html" "src/**/*.html" "src/**/*.css"
