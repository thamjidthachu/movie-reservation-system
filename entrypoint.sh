#!/bin/bash
set -e

# Wait for the database to be ready
until nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Run data insert
python -m scripts.insert_data

# Start the app
exec python run.py
