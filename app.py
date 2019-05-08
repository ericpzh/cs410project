from flask import render_template
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import math
import sys
import time
import metapy
import pytoml
from plsa import topicWords
from searcher import PackageSearcher
from searcher import DescriptionSearcher
import subprocess



app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'any secret string'
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='APP')

@app.route('/test', methods=['GET'])
def test():
    queryContent = request.args.get('data').replace(","," ")
    print("query is: ", queryContent)
    results = app.searcher.search(queryContent)
    return jsonify(results)
    # return jsonify(["n", "m", "s", "l"])

@app.route('/api/description', methods=['GET'])
def descriptionGet():
    queryContent = request.args.get('data')
    print("query is: ", queryContent)
    results = app.searcher2.search(queryContent)
    return jsonify(results)
    # return jsonify([{"title":"nm", "des":"sl", "key":["n", "m", "s", "l"]}])

@app.route('/topic', methods=['GET'])
def topic():
    args = request.args.get('data').split(",")
    print(args)
    return jsonify(args)

if __name__ == '__main__':
    app.searcher = PackageSearcher("config.toml")
    app.searcher2 = DescriptionSearcher("config2.toml")
    # print(app.searcher2.search("framework"))
    app.run()
