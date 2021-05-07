import os
import flask
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# Create the application.
APP = flask.Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@APP.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')


if __name__ == '__main__':
    APP.debug=True
    APP.run()