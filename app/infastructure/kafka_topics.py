from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
class KafkaTopicManager:

    def __init__(self, bootstrap_servers: str):
        self.admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1):
        """Create a Kafka topic if it doesn't exist."""
        try:
            topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
            self.admin_client.create_topics([topic])
            print(f"Created topic: {topic_name}")
        except KafkaException as e:
            print(f"Failed to create topic {topic_name}: {e}")
    def list_topics(self):
        """List existing topics."""
        topics = self.admin_client.list_topics().topics
        print(f"Existing Kafka Topics: {list(topics.keys())}")
        return topics
    
    def existing_topics(self, topic_name: str) -> bool:
        """Check if a Kafka topic exists."""
        topics = self.list_topics()
        return topic_name in topics

