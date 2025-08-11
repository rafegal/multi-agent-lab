#!/bin/bash
# frontend/entrypoint.sh

# Default to development if APP_ENV is not set
APP_ENV=${APP_ENV:-development}

if [ "$APP_ENV" = "development" ]; then
    echo "Running frontend in development mode"
    # In development, use a live-reloading server
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload
else
    echo "Running frontend in production mode"
    # In production, run without auto-reload
    uvicorn main:app --host 0.0.0.0 --port 8080
fi
