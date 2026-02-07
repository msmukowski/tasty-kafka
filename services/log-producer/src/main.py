import random
import time
from datetime import datetime, timezone

from confluent_kafka import Producer
from pydantic import BaseModel

TOPIC = "logs.raw"
SERVICES = ["orders", "payments", "shipping"]
LEVELS = ["INFO", "WARN", "ERROR"]


class LogEvent(BaseModel):
    timestamp: datetime
    service: str
    level: str
    message: str
    trace_id: str


def generate_log() -> LogEvent:
    return LogEvent(
        timestamp=datetime.now(timezone.utc),
        service=random.choice(SERVICES),
        level=random.choice(LEVELS),
        message="Example log message",
        trace_id=str(random.randint(1000, 9999)),
    )


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Sent to {msg.topic()} "
            f"partition={msg.partition()} "
            f"offset={msg.offset()}"
        )


def main():
    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "acks": "all",
        "retries": 5,
        "linger.ms": 20,
        "batch.size": 32_768,
    }
    producer = Producer(producer_config)

    try:
        while True:
            log_event = generate_log()

            producer.produce(
                TOPIC,
                key=log_event.service.encode("utf-8"),
                value=log_event.model_dump_json().encode("utf-8"),
                callback=delivery_report,
            )

            producer.poll(0)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nShutting down, flushing remaining messages...")
        producer.flush()


if __name__ == "__main__":
    main()
