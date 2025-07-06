#!/usr/bin/env bash
# Wait for Kafka Connect
sleep 30
until curl -fs http://connect:8083/connectors >/dev/null; do
  echo "Waiting for Kafka Connect..."
  sleep 5
done

# Create connector
curl -X POST -H "Content-Type: application/json" --data '{
  "name": "inventory-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "inventory",
    "database.server.name": "dbserver1",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "table.include.list": "public.customers",
    "topic.prefix": "dbserver1"
  }
}' http://connect:8083/connectors

export PGPASSWORD="${PGPASSWORD}"

# Wait for PostgreSQL
./wait-for-postgres.sh postgres postgres inventory

sleep 60
# Execute SQL scripts
psql -h postgres -U postgres -d inventory -f /sql-scripts/init.sql

sleep 60
psql -h postgres -U postgres -d inventory -f /sql-scripts/insert.sql



echo "Setup completed successfully!"