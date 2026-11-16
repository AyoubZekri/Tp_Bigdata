
import json
from kafka import KafkaConsumer

TOPIC = "campus-sensors"
TARGET_BUILDING = "Building A"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="tp05-building-filter",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print(f"Filtering building: {TARGET_BUILDING}")

try:
    for message in consumer:
        event = message.value

        if event.get("campus_building") == TARGET_BUILDING:
            print(
                f'Event: {event["event_id"]} | '
                f'Building: {event["campus_building"]} | '
                f'Sensor: {event["sensor_id"]} | '
                f'Temperature: {event["temperature_c"]}°C'
            )

except KeyboardInterrupt:
    print("Consumer stopped by user.")

finally:
    consumer.close()
