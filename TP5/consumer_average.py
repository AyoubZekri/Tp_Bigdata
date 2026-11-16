
import json
from kafka import KafkaConsumer

TOPIC = "campus-sensors"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="tp05-average-test",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

total_temperature = 0
event_count = 0

print("Listening and calculating average temperature...")

try:
    for message in consumer:
        event = message.value

        temperature = event["temperature_c"]
        total_temperature += temperature
        event_count += 1

        average = total_temperature / event_count

        print(
            f'Event: {event["event_id"]} | '
            f'Temperature: {temperature}°C | '
            f'Running Average: {average:.2f}°C | '
            f'Count: {event_count}'
        )

except KeyboardInterrupt:
    print("\nConsumer stopped.")

    if event_count > 0:
        print(f"Total events: {event_count}")
        # pyrefly: ignore[division-by-zero]
        print(f"Average temperature: {total_temperature / event_count:.2f}°C")

finally:
    consumer.close()
