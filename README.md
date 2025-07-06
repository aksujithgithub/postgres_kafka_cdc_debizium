# postgres_kafka_cdc_debizium
A repo that contains a working model cdc model of  postgres, kafka cdc and a python consumer


## Commands to execute
* Install podman or docker 
* cd cdc-demo
* podman-compose up -d --build
* sh register_connector.sh 
* podman cp postgres-sql/init.sql postgres:/tmp/init.sql
* podman exec postgres psql -U postgresuser -d inventory -f /tmp/init.sql
* podman logs python-consumer