import math
import sys
import time
import metapy
import pytoml
from plsa import topicWords
class Searcher:
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




# # query = sys.argv[2]
# query = "express"
# print(query)
# words = getWords(query, 2, 20)
# print(words)
