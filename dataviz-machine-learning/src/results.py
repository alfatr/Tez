
from flask import Blueprint, render_template, redirect, url_for, request

results_bp = Blueprint("results", __name__, static_folder="static", template_folder="templates")

@results_bp.route("/results", methods=['GET', 'POST'])
def results():
        import pandas as pd
        import numpy as np

        ## Bu sayfa şuan statik durumunda
        ## Değerleri kod içinden değiştirmek gerekiyor.

        ## ...