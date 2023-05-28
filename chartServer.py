from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    with open('output.json') as f:
        data = json.load(f)

    filtered_data = []
    for item in data:
        filtered_item = {k: v for k, v in item.items() if v and v != '-'}
        filtered_data.append(filtered_item)

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run("0.0.0.0", port="8888")
