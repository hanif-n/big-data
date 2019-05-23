from time import sleep
from json import dumps
from kafka import KafkaProducer
import os

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

ds_file_path = os.path.join(os.getcwd(), "flixster-dataset\\ratings.txt")

try:
    with open(ds_file_path,"rt") as ds:
        for line in ds:
            producer.send('ratings', value=line)
            print(line)
            sleep(0.0001)
except KeyboardInterrupt:
    print('Keyboard Interrupt, exiting...')
