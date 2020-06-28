from flask import Blueprint, render_template, request, redirect, flash, url_for
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__, static_folder="static", template_folder="templates")


from main import app
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/datasets')
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@upload_bp.route("/upload", methods=['GET', 'POST'])
def upload():
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            
            return redirect(url_for('review.review', dataset_file = filename))
    
    return render_template("upload.html", title="Upload")