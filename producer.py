############################################################
import time
import json
from newsapi import NewsApiClient
from kafka import KafkaProducer

def fetchHeadlines():
    """
    Function to fetch the top headlines from News API

    Returns:
        list : List of headlines from the entertainment category.
    """
    # Initializing NewsApiClient with API key
    news_api = NewsApiClient(api_key=myApiKey)

    # Getting top headlines from the entertainment category
    getTopHeadlines = news_api.get_top_headlines(category='entertainment',
                                               language='en',country='us',page_size=80)
    
    # Checking if the API request was successful
    if getTopHeadlines["status"] == "ok":
        return [x["title"] for x in getTopHeadlines["articles"]]
    return []


class KafkaReadListener():
    def __init__(self):
        # Initializing KafkaProducer with the address of the Kafka broker
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      api_version=(2, 0, 1))

    def streamHeadlines(self):
        """
        Function to stream headlines to Kafka topic (topic1-asgn3)
        """
        # Getting headlines from the fetchHeadlines function
        headlines = fetchHeadlines()
        print("*" *10)
        print(headlines)
        # Sending each headline as a message to the Kafka topic 'topic1-asgn3'
        for hd in headlines:
            # Encoding the headline as UTF-8 before sending
            self.producer.send('topic1-asgn3', hd.encode('utf-8'))



if __name__ == "__main__":
    myApiKey = "828f19f96d804d6585de6a848a5b8961"
    listener = KafkaReadListener()
    while True:
        # Running the streamHeadlines method in a loop with a sleep interval of 60 seconds
        listener.streamHeadlines()
        time.sleep(60)