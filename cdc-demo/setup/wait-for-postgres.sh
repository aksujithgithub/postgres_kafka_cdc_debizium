#!/bin/bash
export PGPASSWORD="${PGPASSWORD}"
until psql -h "$1" -U "$2" -d "$3" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is ready"