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

        return flask.render_template('index.html', pred=run_model_prediction('image.jpg'), image='/static/image.jpg')

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html', pred="Waiting for Image input...", image='/static/blank.png')

@APP.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    APP.debug=True
    APP.run()