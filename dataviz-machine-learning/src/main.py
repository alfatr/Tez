from flask import Flask, render_template
from home import home_bp
from upload import upload_bp
from review import review_bp
from results import results_bp

app = Flask(__name__)
app.register_blueprint(home_bp, url_prefix="")
app.register_blueprint(upload_bp, url_prefix="")
app.register_blueprint(review_bp, url_prefix="")
app.register_blueprint(results_bp, url_prefix="")

@app.route("/test")
@app.route("/")
def test():
    return "<h1>Test<h1>"

if __name__ == "__main__":
    app.run(debug = True)