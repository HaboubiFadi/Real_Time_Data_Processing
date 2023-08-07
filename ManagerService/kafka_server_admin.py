import subprocess
import time

def start_kafka_server():
    kafka_path = "~/Downloads/kafka_2.13-3.5.0"  # Replace with the actual path to your Kafka installation
    zookeeper_cmd = f"{kafka_path}/bin/zookeeper-server-start.sh {kafka_path}/config/zookeeper.properties"
    kafka_cmd = f"{kafka_path}/bin/kafka-server-start.sh {kafka_path}/config/server.properties"

    # Start ZooKeeper
    subprocess.Popen(zookeeper_cmd, shell=True)

    # Wait for ZooKeeper to start (you can adjust the sleep time based on your machine's performance)
    time.sleep(5)

    # Start Kafka server
    subprocess.Popen(kafka_cmd, shell=True)

if __name__ == "__main__":
    start_kafka_server()