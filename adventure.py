from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    Response
    )
from werkzeug import secure_filename
from datetime import datetime
from termcolor import colored
import os
import time

app = Flask(__name__)

app.config['UPLOAD_DIR'] = os.getenv('ADV_UPLOAD_DIR', '/tmp')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'odt'])


def allowed_file(filename):
    ''' Naive test to check whether a file is in accpted formats'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def slomo(template_file):
    ''' Make the slow motion effect and coloriz text'''
    with open(template_file) as f:
        for line in f:
            time.sleep(0.2)
            yield colored(line, 'green')


@app.route('/apply', methods=['POST'])
def upload():
    ''' Accept uploads'''
    ua = request.user_agent.string

    if not (ua.startswith('curl') or ua.startswith('Wget')):
        return redirect(url_for('no-adventure'))

    if request.method == 'POST' and 'file' in request.files:
        file_ = request.files['file']
        if file and allowed_file(file_.filename):
            filename = str(datetime.now().strftime('%Y%m%d_%H%M%S')) + '_' +\
                secure_filename(file_.filename)
            file_.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            return render_template('thank-you.txt')
    else:
        return render_template('oops.txt')


@app.route('/adventure')
def adventure():
    ua = request.user_agent.string

    if ua.startswith('curl') or ua.startswith('Wget'):
        return Response(slomo('templates/adventure.txt'))
    else:
        return redirect(url_for('no-adventure'))


@app.route('/no-adventure')
def no_adventure():
    return render_template('no-adventure.html')


@app.route('/')
def root():
    ua = request.user_agent.string
    return ua


if __name__ == '__main__':
    app.run(debug=True, port=8989)
