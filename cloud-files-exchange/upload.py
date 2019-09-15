# Imports the Google Cloud client library
from google.cloud import storage

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'xlsx', 'docx', 'pptx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file(filename):
    if filename == '':
        print('No file selected for uploading')
        return False

    if filename and allowed_file(filename):
        return True

    else:
        print('Allowed file types are txt, csv, pdf, png, jpg, jpeg, gif, svg, xlsx, docx and pptx')
        return False


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Instantiates a client
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print('Uploading file {} to bucket {} ...'.format(
        source_file_name,
        bucket_name))

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to bucket {}.'.format(
        source_file_name,
        bucket_name))



def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    filesList = [[]]

    for blob in blobs:
        fileName = '{}'.format(blob.name)
        fileSize = '{} bytes'.format(blob.size)
        fileUpdated = '{}'.format(blob.updated)

        filesList.append([fileName, fileSize, fileUpdated])

    return (filesList)


def create_bucket(bucket_name):
    # Instantiates a client
    storage_client = storage.Client()
    # Creates the new bucket
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created.'.format(bucket.name))


if __name__ == '__main__':
    print('This is not the application main module. Please execute app.py.')