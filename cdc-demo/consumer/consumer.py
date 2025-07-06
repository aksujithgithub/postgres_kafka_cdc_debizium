from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import sys
import time

def create_consumer():
    conf = {
        'bootstrap.servers': 'kafka:9092',  # Using service name from compose file
        'group.id': 'python-consumer-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'socket.keepalive.enable': True,
        'reconnect.backoff.ms': 1000,
        'reconnect.backoff.max.ms': 10000
    }

    consumer = Consumer(conf)
    return consumer

def wait_for_kafka():
    """Wait for Kafka to become available"""
    max_retries = 10
    retry_count = 0
    consumer = None
    
    while retry_count < max_retries:
        try:
            consumer = create_consumer()
            # Test connection by getting metadata
            consumer.list_topics(timeout=10)
            return consumer
        except Exception as e:
            retry_count += 1
            print(f"Attempt {retry_count}/{max_retries}: Kafka not available yet - {str(e)}")
            time.sleep(5)
    
    raise Exception("Failed to connect to Kafka after multiple attempts")

def consume_messages(consumer, topics):
    try:
        consumer.subscribe(topics)
        print(f"Subscribed to topics: {topics}")

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                try:
                    message = json.loads(msg.value())
                    # Process message as before
                    print(f"Received message: {message}")
                    
                except json.JSONDecodeError:
                    print(f"Raw message: {msg.value()}")

    except KeyboardInterrupt:
        print('%% Aborted by user\n')
    finally:
        consumer.close()

if __name__ == '__main__':
    print('Python Consumer is sleeping for 120 seconds...')
    time.sleep(120)
    print('Starting Python Consumer...')
    try:
        consumer = wait_for_kafka()
        consume_messages(consumer, ['dbserver1.public.customers'])
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)