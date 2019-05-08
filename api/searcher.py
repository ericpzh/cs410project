import math
import sys
import time
import metapy
import pytoml
import json
from plsa import topicWords
class PackageSearcher:
    def __init__(self, cfg):
        self.idx = metapy.index.make_inverted_index(cfg)
        self.ranker = metapy.index.OkapiBM25()
        with open("package/package.dat", 'r') as f:
            documents = []
            for i in f.readlines():
                documents.append(i.replace('\n', ''))
        self.documents = documents

    def search(self, queryContent, number_of_topics=3, number_of_terms=10):
        query = metapy.index.Document()
        query.content(queryContent)
        ranker = self.ranker
        query = metapy.index.Document()
        query.content(queryContent)
        print("query")
        results = ranker.score(self.idx, query)
        print("get result", results)
        rel_doc = []
        for id, score in results:
            rel_doc.append(self.documents[id])
        return topicWords(rel_doc, queryContent, number_of_topics, number_of_terms)

class DescriptionSearcher:
    def __init__(self, cfg):
        self.idx = metapy.index.make_inverted_index(cfg)
        self.ranker = metapy.index.OkapiBM25()

        with open("description/description.dat", 'r') as f:
            documents = []
            for i in f.readlines():
                documents.append(i.replace('\n', ''))
        with open("parsed_packages.json", 'r') as f:
            packages = json.loads(f.readline())
        self.packages = packages
        self.documents = documents


    def search(self, queryContent, number_of_topics=3, number_of_terms=10):
        query = metapy.index.Document()
        query.content(queryContent)
        ranker = self.ranker
        query = metapy.index.Document()
        query.content(queryContent)
        results = ranker.score(self.idx, query, 10)
        print("get result", results)
        rel_doc = []
        for id, score in results:
            rel_doc.append(self.packages[id])
        return rel_doc




# # query = sys.argv[2]
# query = "express"
# print(query)
# words = getWords(query, 2, 20)
# print(words)
