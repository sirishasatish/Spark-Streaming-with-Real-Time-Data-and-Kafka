######################################################################

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, udf, expr, count, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
import spacy
import string

# Loading the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Defining the Kafka topics and Spark application name
INPUT_KAFKA_TOPIC = "topic1-asgn3"
SPARK_APP_NAME = "NewsConsumer"

# Create a Spark session
spark = SparkSession.builder.appName(SPARK_APP_NAME).getOrCreate()

# Define the schema for the incoming Kafka messages
schema = StructType([StructField("value", StringType(), True)])

# Read data from Kafka as a DataFrame
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", INPUT_KAFKA_TOPIC) \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

print("Schema of Kafka DataFrame:")
kafka_df.printSchema()


# Define a User Defined Function to extract named entities using spaCy
def extractNamedEntities(text):
    """
    Function to extract Named Entities from text using spaCy.

    Parameters:
        string : input text
    Returns:
        list : List of Named Entities extracted from the input text.
    """
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation)).lower()
    doc = nlp(text)
    # Extract named entities excluding stop words
    entities = [ent.text for ent in doc.ents if not any(token.is_stop for token in doc if token.text in ent.text)]
    return entities


extractNamedEntitiesUdf = udf(extractNamedEntities, ArrayType(StringType()))

# Apply the UDF to extract named entities
namedEntitiesDf = kafka_df.withColumn("named_entities", explode(extractNamedEntitiesUdf("value"))).select("value", "named_entities")


entityCountDf = namedEntitiesDf.groupBy("named_entities").agg(count("*").alias("count"))
jsonDf = entityCountDf.withColumn("value", to_json(struct("named_entities", "count")))

checkpoint_location = "/Users/sirishasatish/my_checkpoint_dir"

# Display the results
query = jsonDf.writeStream \
    .outputMode("complete") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "topic2-asgn3") \
    .option("checkpointLocation", checkpoint_location) \
    .start()


# Await termination of the query
query.awaitTermination()