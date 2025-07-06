from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import time

def create_consumer():
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'python-consumer-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'topic.metadata.refresh.interval.ms': '30000'  # Check for topic every 30s
    }
    return Consumer(conf)

def wait_for_topic(consumer, topic, timeout=120):
    """Wait for topic to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        metadata = consumer.list_topics(timeout=10)
        if metadata.topics.get(topic) is not None:
            print(f"Topic '{topic}' is available")
            return True
        print(f"Waiting for topic '{topic}'...")
        time.sleep(5)
    raise KafkaException(KafkaError(KafkaError._TIMED_OUT, 
                  f"Topic '{topic}' not available after {timeout} seconds"))

def process_message(msg):
    """Process incoming Kafka message"""
    try:
        data = json.loads(msg.value())
        print(f"Received message: {data}")
    except json.JSONDecodeError:
        print(f"Received raw message: {msg.value()}")

def main():
    print("Starting Kafka Consumer...")
    consumer = create_consumer()
    topic = "dbserver1.public.customers"

    try:
        # Wait for topic to exist before subscribing
        wait_for_topic(consumer, topic)
        
        consumer.subscribe([topic])
        
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PARTITION:
                    print("Topic lost, attempting to resubscribe...")
                    wait_for_topic(consumer, topic)
                    consumer.subscribe([topic])
                    continue
                else:
                    raise KafkaException(msg.error())
            process_message(msg)
            
    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        consumer.close()

if __name__ == "__main__":
    print("Sleeping consumer for 120 secs")
    time.sleep(120)
    main()