import subprocess
import urllib.request
import tarfile
import os

# Define Kafka version
kafka_version = "2.8.0"
scala_version = "2.12"

# Download Kafka
url = f"https://archive.apache.org/dist/kafka/{kafka_version}/kafka_{scala_version}-{kafka_version}.tgz"
download_path = "kafka.tgz"
urllib.request.urlretrieve(url, download_path)

# Extract Kafka
with tarfile.open(download_path, "r:gz") as tar:
    tar.extractall()

# Change to Kafka directory
kafka_dir = f"kafka_{scala_version}-{kafka_version}"
os.chdir(kafka_dir)
print(os.getcwd())
# Start Zookeeper
subprocess.run(["/bin/zookeeper-server-start.sh", "config/zookeeper.properties"], shell=True)

# Start Kafka server
subprocess.run(["/bin/kafka-server-start.sh", "config/server.properties"], shell=True)
