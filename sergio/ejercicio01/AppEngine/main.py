
from flask import Flask, flash, request, redirect, url_for
from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.utils import secure_filename
from google.cloud import storage
from google.cloud import pubsub_v1
import os

ALLOWED_EXTENSIONS = set(['csv'])
PROJECT_ID = 'psychic-force-228722'
TOPIC_NAME = 'TPejercicio01'

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            client = storage.Client(project=PROJECT_ID)
            bucket = client.get_bucket('testing01_228722')
            blob_name = 'to_process/' + filename
            blob = bucket.blob(blob_name)
            blob.upload_from_string(
                file.read(), #file_stream,
                content_type='text/csv')
            blob.make_public()
            url = blob.public_url

            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
            data = blob_name.encode('utf-8')
            publisher.publish(topic_path, data=data)
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>GCP Upload csv file</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
