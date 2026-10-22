#!/usr/bin/env bash
# ============================================================
# build.sh — Render build script (runs before the web service starts)
# ============================================================
set -o errexit   # Exit immediately on any error

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input --settings=jobmailer.settings.prod

echo "==> Applying database migrations..."
python manage.py migrate --no-input --settings=jobmailer.settings.prod

echo "==> Build complete ✓"
