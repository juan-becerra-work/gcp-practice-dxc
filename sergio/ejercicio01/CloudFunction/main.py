import base64
from google.cloud import storage

def process_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    PROJECT_ID = 'psychic-force-228722'
    BUCKET_ID = 'testing01_228722'
    blob_name = base64.b64decode(event['data']).decode('utf-8')
    
    client = storage.Client(project=PROJECT_ID)
	# bucket = client.get_bucket(BUCKET_ID)
    bucket = client.get_bucket('testing01_228722')
    blob = bucket.blob(blob_name)
    print(blob_name)
    new_name = blob_name.replace("to_process","processed")
    new_blob = bucket.rename_blob(blob, new_name)
    print ("the file {} moved to {}".format(blob_name, new_name))