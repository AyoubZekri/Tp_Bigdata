
import json
import random
from kafka import KafkaProducer

import sys

TOPIC = sys.argv[1] if len(sys.argv) > 1 else "campus-sensors-one"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    acks="all",
)

try:
    for event_id in range(1, 31):
        event = {
            "event_id": event_id,
            "sensor_id": f"sensor-{random.randint(1, 4):02d}",
            "temperature_c": round(random.uniform(18, 42), 2),
            "humidity_pct": round(random.uniform(25, 85), 2),
        }

        metadata = producer.send(TOPIC, value=event).get()

        print(
            f"Event {event_id} | "
            f"Topic: {metadata.topic} | "
            f"Partition: {metadata.partition}"
        )

    print("30 events sent successfully!")

finally:
    producer.close()
