#!/bin/bash

postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

# psql -U postgres -c "CREATE EXTENSION vector;" || true

alembic upgrade head

gunicorn src.main:app --preload --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000