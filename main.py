import os
from app import app
from flask import (
    flash, request, redirect, url_for, render_template, send_from_directory, jsonify, session
)
from werkzeug.utils import secure_filename
import subprocess

# Get environment variables
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8002")
PORT = os.environ.get("PORT", 8002)
ALLOWED_EXTENSIONS = {'mp4'}
output = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        render_template('output.html', output="siuu")
        # Run the script
        result = subprocess.run(['python3', 'people_counter.py', '--prototxt', 'detector/MobileNetSSD_deploy.prototxt', '--model', 'detector/MobileNetSSD_deploy.caffemodel', '--input', os.path.join(app.config['UPLOAD_FOLDER'], filename)],capture_output=True)
        #print(result.stdout.decode('utf-8'))
        #return render_template('output.html', output=result.stdout.decode('utf-8'))
        session['output'] = result.stdout.decode('utf-8')
        return redirect(url_for('show_output'))
    

@app.route('/output',methods=['GET'])
def show_output():
    output = session.get('output','None')
    return render_template('output.html',output=output)

@app.route('/output',methods=['POST'])
def redirect_home():
    return redirect(url_for('upload_form'))

if __name__ == '__main__':
    app.run(debug=True, port=PORT,host="0.0.0.0")
