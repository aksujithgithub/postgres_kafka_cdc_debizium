# postgres_kafka_cdc_debizium
A repo that contains a working model cdc model of  postgres, kafka cdc and a python consumer


## Commands to execute if execute manually
* Install podman or docker 
* cd cdc-demo
* podman-compose up -d --build
* sh register_connector.sh 
* podman cp sql-scripts/update.sql postgres:/tmp/update.sql
* podman exec postgres psql -U postgres -d inventory -f /tmp/update.sql
* podman logs python-consumer
* kafka UI https://localhost:8080

## cleanup
* podman-compose down

## Debugging commands:
* curl -s http://localhost:8083/connectors/inventory-connector/status | jq

* curl -s http://localhost:8083/connectors/inventory-connector | jq

* podman exec -it kafka bash

* kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic dbserver1.public.customers --from-beginning
* kafka-topics.sh --bootstrap-server localhost:9092 --list

* podman exec postgres psql -U postgres inventory -c "SELECT * FROM customers;"
* podman logs setup
* podman logs python-consumer