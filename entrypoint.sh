#!/bin/sh

# Default to production mode if APP_ENV is not set
if [ -z "${APP_ENV}" ]; then
  APP_ENV="production"
fi

echo "Starting application in ${APP_ENV} mode..."

if [ "${APP_ENV}" = "development" ]; then
  # In development, run with --reload
  uvicorn vitra_ai.main:app --host 0.0.0.0 --port 8000 --reload
else
  # In production, run without --reload
  uvicorn vitra_ai.main:app --host 0.0.0.0 --port 8000
fi
