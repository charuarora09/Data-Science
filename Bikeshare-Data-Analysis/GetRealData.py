import requests
import time
import json
from kafka.producer import  KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

n = 1000
while n > 0:
	r1 = requests.get(url='http://feeds.bayareabikeshare.com/stations/stations.json', stream=True).content
	r1JSON = json.loads(r1)
	print r1JSON
	print len(r1JSON['stationBeanList'])
	for x in r1JSON['stationBeanList']:
		producer.send("BDProject", json.dumps(x))
	time.sleep(120)