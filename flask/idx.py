import os
import flask
from werkzeug.utils import secure_filename
from nn_covid import run_model_prediction

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Create the application.
APP = flask.Flask(__name__)


@APP.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        f.save(secure_filename('image.jpg'))

        return flask.render_template('index.html', pred=run_model_prediction('image.jpg'))

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html', pred="Input image")


if __name__ == '__main__':
    APP.debug=True
    APP.run()