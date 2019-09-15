# Imports the Google Cloud client library
from flask import Flask, render_template, request, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from upload import upload_blob, list_blobs
import os


# The name of the bucket
bucket_name = 'cloud-files-exchange-input'

# Instantiates a client
app = Flask(__name__)

# Max file size = 2MB
#app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
MAX_FILE_SIZE=2000000

# Uses Bootstrap
Bootstrap(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        if request.files:
            file = request.files["file"]

            filename = secure_filename(file.filename)
            filepath = './uploads/' + filename

            file.save (filepath)
            print (os.path.getsize(filepath))

            upload_blob(bucket_name, filepath, filename)
            os.remove(filepath)

            return render_template("upload.html", Message="File uploaded successfully!", FilesUploaded=list_blobs(bucket_name))

        else:
            return render_template("upload.html", Message='File does not exists', FilesUploaded=list_blobs(bucket_name))

    return render_template("upload.html", Message="Ready to upload file", FilesUploaded=list_blobs(bucket_name))


app.secret_key = "12345"


if __name__ == '__main__':
    app.run(debug=True)