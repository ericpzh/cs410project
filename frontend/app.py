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
from searcher import Searcher
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
    print("query is: ",queryContent)
    # base_path = "./../meta/"
    # cfg = base_path + "config.toml"
    # inv_idx = metapy.index.make_inverted_index(cfg)
    # fwd_idx = metapy.index.make_forward_index(cfg)
    # ranker = metapy.index.OkapiBM25(k1=2,b=0.75,k3=500)
    # query = metapy.index.Document()
    # query.content("express")
    # print("query")
    # results = ranker.score(inv_idx, query)
    # results = app.searcher.search("express")
    subprocess.run(["python", "searcher.py"], capture_output=True)
    # print("get result", search())
    return jsonify("nmsl")


@app.route('/topic', methods=['GET'])
def topic():
    args = request.args.get('data').split(",")
    print(args)
    return jsonify(args)

def search():
    return app.searcher.search("express")

if __name__ == '__main__':
    # app.searcher = Searcher("config.toml")
    app.run(port=5000)
    # query = "express"
    # print("result", search())
