from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime
import json

consumer = KafkaConsumer('BDProject')

es = Elasticsearch()

bikemap = {
    'mappings': {
    "bikedata": {
        "properties": {
            "lastCommunicationTime": { "type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
            "Coordinates": {'type': 'geo_point'},
        }
        }
    }
}

i=1
es.indices.create(index='bikedata-index', body=bikemap)
for message in consumer:
    if(i==64):
        i = 1
        es.indices.delete(index='bikedata-index')
        es.indices.create(index='bikedata-index', body=bikemap)
    result = json.loads(message.value)
    result['Coordinates'] = str(result['latitude'])+','+str(result['longitude'])
    res = es.index(index="bikedata-index", doc_type='bikedata', id=i, body=result)
    print res
    i+=1

