from flask import Blueprint, render_template, redirect, url_for, request
review_bp = Blueprint("review", __name__, static_folder="static", template_folder="templates")

import pandas as pd
import numpy as np
import os
import os.path



@review_bp.route("/review", methods=['GET', 'POST'])
def review():
    from main import app

    def analysis(dataset_file_name : str):
        if dataset_file_name == '' :
            return redirect(url_for('upload.upload'))

        df = pd.DataFrame([])

        if dataset_file_name.endswith('.csv'):
            df = pd.read_csv(os.path.join(app.root_path, 'static\datasets', dataset_file_name))
        
        elif dataset_file_name.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(app.root_path, 'static\datasets', dataset_file_name))

        return df

    dataset_file_name = request.args.get('dataset_file', type = str)
    dataframe = analysis(dataset_file_name)

    if request.method == 'POST':
        chosen_columns = request.form.getlist('chosen_columns')
        return redirect(url_for('results.results', dataset = dataset_file_name, chosen_columns = chosen_columns))

    return render_template(
        "review.html",
        title = "Reviewing Dataset",
        dataset_file_name = dataset_file_name,
        uploaded_df = dataframe,
        characteristics_df = dataframe)