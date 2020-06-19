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
        "home.html",
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

    # Asıl back-end tarafı burda olmalı
    # Bunun için ilk önce jupyter üzerinde bir proje yapılsa iyi olabilir.
    # Şuan için ilk araştırılması gereken şeyler
    # Meta-learning, learning to rank, feature vectors, training, optimizing
    df = pd.read_csv(dataset_file)
    JSONdata = df.to_dict(orient='records')
    
    def get_column_values( columns : []) -> []:
        column_values = []
        
        for col in columns:
            datatype = str(df[col].dtype)
            groups = df.groupby(col).size().shape[0]
            missing_values = df[col].isnull().sum()
            
            #Veri tipine göre değişen değerler, bu sınırlamalar düzeltilmeli
            
            if(df[col].dtypes != np.object):
                min_value = df[col].min()
                max_value = df[col].max()
                mean = df[col].mean()
                std = df[col].std()
                _range = df[col].max() - df[col].min()
                scale = mean / _range
            else:
                min_value = np.NaN
                max_value = np.NaN
                mean = np.NaN
                std = np.NaN
                _range = np.NaN
                scale = np.NaN
                
            column_values.append(
                {
                    'Name' : col,
                    'Datatype' : datatype,
                    'Min': min_value,
                    'Max': max_value,
                    'Mean' : mean,
                    'Std' : std,
                    'Range' : _range,
                    'Range Scale' : scale,
                    'Groups' : groups,
                    'Missing Values' : missing_values
                })
            
        return column_values


    # En başta seçilen sütunlara göre karakteristik değerlerini oluştur.
    # Daha çok eklenebilir.

    column_values = get_column_values(df.columns)
    summary = pd.DataFrame(column_values)

    scores = [1, 5, 6, 7]

    if request.method == 'POST':
        return redirect(url_for('results'))

    return render_template(
        "upload_successful.html",
        title = "Upload Successful",
        dataset_file = dataset_file,
        dataframe_var = df,
        summary = summary,
        scores = scores,
        data = JSONdata,
        JSONdata = JSONdata)

@app.route("/results/POST?", methods=['GET', 'POST'])
def results(data, columns, scores):
        return render_template(
        "results.html",
        data = data,
        columns = columns,
        scores = scores)

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)