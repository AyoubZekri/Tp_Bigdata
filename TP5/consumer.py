
import json
from kafka import KafkaConsumer

TOPIC = "campus-sensors"

TARGET_BUILDING = "Building A"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="tp05-campus-monitor",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print(f"Listening to topic: {TOPIC}")
print(f"Filtering building: {TARGET_BUILDING}")

try:
    for message in consumer:

        event = message.value

        if event.get("campus_building") != TARGET_BUILDING:
            continue

        temperature = event["temperature_c"]

        print(
            f'{event["timestamp"]} | '
            f'{event["sensor_id"]} | '
            f'{event["campus_building"]} | '
            f'T={temperature}°C | '
            f'RH={event["humidity_pct"]}%'
        )

        if temperature >= 35:
            print("ALERT: High temperature detected!")

except KeyboardInterrupt:
    print("Consumer stopped by user.")

finally:
    consumer.close()
