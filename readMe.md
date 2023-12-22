# Initial Setup - 
1. Start the Kafka Environment
   - Navigate to the Kafka folder.
   - Start Zookeeper: `bin/zookeeper-server-start.sh config/zookeeper.properties`
   - Start Kafka: `bin/kafka-server-start.sh config/server.properties`
2. Create Kafka Topics:
   - Create read topic: `bin/kafka-topics.sh --create --topic topic1-asgn3 --bootstrap-server localhost:9092`
   - Create write topic: `bin/kafka-topics.sh --create --topic topic2-asgn2 --bootstrap-server localhost:9092`
3. Ensure the topics are created:
    `bin/kafka-topics.sh --bootstrap-server localhost:9092 --list`


# Python-
1. import necesssary libraries like spacy, NewsApiClient, KafkaProducer
2. Run the producer file: python producer.py
3. Ensure the data is straming in topic1-asgn3 in kafka:
    bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic1-asgn3
4. After running the producer run the consumer file using the following script:
    `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 consumer.py localhost:9092 subscribe topic2-asgn3` (Modify the above script accoridng to the spark version installed in your computer)
5. Ensure the Named Entites are extracted in topic2-asgn3 by running the following command - 
    `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic2-asgn3` 

# ELK Stack:
1. Navigate to the ElasticSearch directory.
2. Run: `bin/elasticsearch`
3. Verify if Elastic sesrch is running fine in `localhost:9200`

# Logstash:
1. Navigate to the LogStash directory.
2. Run: `bin/logstash`
3. Use the logstash.conf file in the current directory.

# Kibana:
1. Navigate to the Kibana directory.
2. Run: `/bin/kibana`



# Kibana: View Data
1. Click on the top left corner icon.
2. In the left toolbar, scroll to the bottom and click on "Stack Management," then click on "Index Management"
3. Verify the presence of the index i.e., `assignment3-part1`
4. Click on "Discover."
5. Create a Visualization using Lens using appropriate fields.

# Kibana: Dashboard
1. Click on the "Dashboard" view and create a bar chart and donut.
2. Capture the necessary insights for 15, 30, 45 and 60 mintues.