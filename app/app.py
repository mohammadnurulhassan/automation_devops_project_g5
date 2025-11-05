from flask import Flask, render_template
from data import fetch_data

app = Flask(__name__)

@app.route('/')
def index():
    data = fetch_data()

    return render_template(
        'index.html',
        page_data = data,
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)