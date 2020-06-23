import os
import tempfile

from flask import Flask, request, redirect, flash, url_for, jsonify, make_response, render_template
from werkzeug.utils import secure_filename

from classifier import Classifier

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir() + '/tmp-images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
classifier = Classifier('data/saved-model.h5', 'data/class-labels.json')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health')
def health():
    return jsonify(status="OK")


@app.route("/")
def root():
    return health()


@app.route('/api/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return client_error("no file found in the request")

    file = request.files["file"]
    if file.filename == '':
        return client_error("no file selected")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        recognised_image = classifier.predict(filepath)
        os.remove(filepath)

        return jsonify(subject=recognised_image)


def client_error(message):
    return make_response(jsonify(error=message), 400)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    app.run()
