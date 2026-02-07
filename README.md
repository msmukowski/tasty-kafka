# tasty-kafka

A project for learning Apache Kafka.

## Prerequisites

- Docker Desktop (with Rosetta enabled on Apple Silicon)

## Getting started

```bash
docker compose up -d
```

Kafka will be available at `localhost:9092`. The image runs in KRaft mode (no ZooKeeper).

> **Apple Silicon:** the image forces `platform: linux/amd64` — the native ARM build crashes the JVM (SIGILL).

## Useful commands

```bash
# Create a topic
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --create --topic test-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 --replication-factor 1

# List topics
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --list --bootstrap-server localhost:9092

# Describe a topic
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --describe --topic test-topic \
  --bootstrap-server localhost:9092

# Produce messages (type lines, Ctrl+C to stop)
docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh \
  --topic test-topic --bootstrap-server localhost:9092

# Consume messages
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --topic test-topic --bootstrap-server localhost:9092 \
  --from-beginning
```

## Stopping

```bash
docker compose down        # stop the container
docker compose down -v     # stop + remove data
```