import subprocess
import urllib.request
import tarfile
import os

# Define Kafka version
kafka_version = "2.8.0"
scala_version = "2.12"

# Download Kafka
download_path = "kafka.tgz"
if not os.path.exists(download_path):
    url = f"https://archive.apache.org/dist/kafka/{kafka_version}/kafka_{scala_version}-{kafka_version}.tgz"
    
    urllib.request.urlretrieve(url, download_path)

    # Extract Kafka
    with tarfile.open(download_path, "r:gz") as tar:
        tar.extractall()

# Change to Kafka directory
kafka_dir = f"kafka_{scala_version}-{kafka_version}"
# os.chdir(kafka_dir)
zookeeper = os.getcwd()+f"\{kafka_dir}\\bin\zookeeper-server-start.sh"
print(zookeeper)
# Start Zookeeper
subprocess.run(['bash', zookeeper, "config/zookeeper.properties"])

# Start Kafka server
# subprocess.run(["wsl", "bin/kafka-server-start.sh", "config/server.properties"])


