from flask import Flask, render_template, url_for
from flask_assets import Bundle, Environment

app = Flask(__name__)

js = Bundle(
        'js//libraries//jquery-3.5.1.slim.min.js',
        'js//libraries//popper.min.js',
        'js//libraries//bootstrap.min.js',
        'js//dataviz//d3.v4.js',
        'js//dataviz//scripts.js',
        'js//dataviz//basic-histogram.js',
        'js//dataviz//basic-barplot.js',
        'js//dataviz//basic-scatter.js',
        'js//dataviz//basic-line.js',
        'js//dataviz//basic-bubble.js',
    output = 'gen/main.js')

css = Bundle(
        'css//bootstrap.min.css',
        'css//style.css',
    output = 'generated/style.css')

assets = Environment(app)
assets.register("css_asset", css)
assets.register("js_asset", js)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)