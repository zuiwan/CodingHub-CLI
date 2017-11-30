from kafka import KafkaConsumer

import json

consumer = KafkaConsumer("test123123123", bootstrap_servers=['47.92.31.158:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=False)

for msg in consumer:
    print json.loads(msg.value).get("@timestamp").strip("\n"),json.loads(msg.value).get("log").strip("\n")