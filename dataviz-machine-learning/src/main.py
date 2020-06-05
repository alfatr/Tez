# Flask ve url, bundling işlemleri
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from os.path import join, dirname, realpath

# Dosya yükleme işlemleri
from werkzeug.utils import secure_filename

# Makine öğrenmesi ve data analizi
import pandas as pd
import numpy as np

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/datasets/..')
ALLOWED_EXTENSIONS = {'csv', 'xls'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])

def homepage():
    return render_template(
        "layout.html",
        title = "Home")

@app.route("/select_dataset", methods=['GET', 'POST'])
def select_dataset():
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
            
            return redirect(url_for('upload_successful', dataset_file = filename))
    
    return render_template(
        "select_dataset.html",
        title = "Select Dataset")
    

@app.route("/upload_successful/<path:dataset_file>", methods=['GET', 'POST'])
def upload_successful(dataset_file):
    if dataset_file == '' :
        return redirect(url_for('select_dataset'))
    
    df = pd.read_csv(dataset_file)
    JSONdata = df.to_dict(orient='records')

    

    return render_template(
        "upload_successful.html",
        title = "Upload Successful",
        dataset_file = dataset_file,
        dataframe_var = df,
        data = JSONdata,
        JSONdata = JSONdata)

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)