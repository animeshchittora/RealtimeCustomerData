import logging
from azure.storage.blob import BlobServiceClient
from azure.functions import ServiceBusMessage
import os
import json

def main(msg: ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    print(msg.get_body().decode('utf-8'))
    blob_service_client  = BlobServiceClient.from_connection_string(os.environ['blob_secret'])
    blob_client = blob_service_client.get_blob_client("realtimedata",blob="customerdata.txt")
    data_to_upload=json.dumps(msg.get_body().decode('utf-8'))
    try:
        blob_client.upload_blob(msg.get_body(),overwrite=True)
    except:
        print("Data not uploaded to blob")

    print("data uploaded to blob successfully")