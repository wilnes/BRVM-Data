#!/bin/sh
set -e

host="$1"
shift

echo "Waiting for Postgres at $host..."
until pg_isready -h "$host" -U "$POSTGRES_USER"; do
  sleep 2
done

echo "Postgres is ready!"
exec "$@"
