from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import os

consumer = KafkaConsumer(
    'ratings',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='flixster',
     value_deserializer=lambda x: loads(x.decode('utf-8')))


ds_batch_folder_path = os.path.join(os.getcwd(), "flixster-dataset-batch")
batch_limit = 250000
n_batch = 0
n_line = 0
try:
    while True:
        for message in consumer:
            if n_line >= batch_limit:
                ds_batch.close()
                n_line = 0
                n_batch += 1
                continue
            elif n_line == 0:
                ds_batch_path = os.path.join(ds_batch_folder_path, ('ratings-batch-' + str(n_batch) + '.txt'))
                ds_batch = open(ds_batch_path, "w")
            message = message.value
            ds_batch.write(message)
            n_line += 1
            print('Batch ' + str(n_batch) + ' Line ' + str(n_line) + ' : ' + str(message[:-1]))
except KeyboardInterrupt:
    ds_batch.close()
    print('Keyboard Interrupt, exiting...')
