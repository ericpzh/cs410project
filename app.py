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

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config['SECRET_KEY'] = 'any secret string'
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='APP')

@app.route('/api/package', methods=['GET'])
def packageGet():
    queryContent = request.args.get('data').replace(","," ")
    print("query is: ", queryContent)
    searcher = PackageSearcher("config.toml")
    results = searcher.search(queryContent)
    return jsonify(results)

@app.route('/api/description', methods=['GET'])
def descriptionGet():
    queryContent = request.args.get('data')
    print("query is: ", queryContent)
    searcher =  DescriptionSearcher("config2.toml")
    results = searcher.search(queryContent)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
