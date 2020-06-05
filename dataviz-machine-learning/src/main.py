# Flask ve url, bundling işlemleri
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_assets import Bundle, Environment
# Dosya yükleme
from werkzeug.utils import secure_filename
import os
# Blueprints

app = Flask(__name__)
UPLOAD_FOLDER = 'C:\\Users\\Weaver\\Desktop'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('/home'))
    
    
    return render_template("master.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)