#!/bin/bash

# Get the parent directory of the current script
PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Execute zookeeper
"$PARENT_DIR/kafka_2.12-2.8.0/bin/zookeeper-server-start.sh config/zookeeper.properties"
# Execute kafka
"$PARENT_DIR/kafka_2.12-2.8.0/bin/kafka-server-start.sh config/server.properties"
