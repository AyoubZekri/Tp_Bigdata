
import json
import sys
from kafka import KafkaConsumer

TOPIC = "campus-sensors"

GROUP_ID = sys.argv[1] if len(sys.argv) > 1 else "group-A"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    # enable_auto_commit=True,
    group_id=GROUP_ID,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print(f"Consumer started | Group: {GROUP_ID}")

try:
    for message in consumer:
        event = message.value
        temperature = event["temperature_c"]
        print(
            f"Group={GROUP_ID} | "
            f"Event={event['event_id']} | "
            f"Sensor={event['sensor_id']} | "
            f"Temperature={event['temperature_c']}°C | "
            f"Partition={message.partition}"
        )

        if temperature >= 35:
            print("ALERT: High temperature detected!")


except KeyboardInterrupt:
    print(f"\nConsumer {GROUP_ID} stopped.")

finally:
    consumer.close()
