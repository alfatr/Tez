from flask import Flask, render_template

app = Flask(__name__)

from views import home
from views import upload
from views import review
from views import results

from views import example

app.register_blueprint(home.home_bp, url_prefix="")
app.register_blueprint(upload.upload_bp, url_prefix="")
app.register_blueprint(review.review_bp, url_prefix="")
app.register_blueprint(results.results_bp, url_prefix="")

@app.route("/test")
@app.route("/")
def test():
    return "<h1>Test<h1>"

if __name__ == "__main__":
    app.run(debug = True)