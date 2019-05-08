import math
import sys
import time
import metapy
import pytoml
from plsa import topicWords


def getDocuments():
    print("getDocuments")
    with open(base_path + "package/package.dat", 'r') as f:
        documents = []
        for i in f.readlines():
            documents.append(i.replace('\n', ''))
    return documents

def search(documents, queryContent):
    cfg = base_path + "config.toml"
    inv_idx = metapy.index.make_inverted_index(cfg)
    fwd_idx = metapy.index.make_forward_index(cfg)
    ranker = metapy.index.OkapiBM25(k1=2,b=0.75,k3=500)
    top_k = 10
    query = metapy.index.Document()
    query.content(queryContent)
    print("query")
    results = ranker.score(inv_idx, query, top_k)
    print("get result", results)
    rel_doc = []
    for id, score in results:
        rel_doc.append(documents[id])
    return rel_doc

def getWords(queryContent, number_of_topics=3, number_of_terms=10):
    print("get words")
    rel_doc = search(getDocuments(), queryContent)
    print(rel_doc)

    return topicWords(rel_doc, queryContent, number_of_topics, number_of_terms)


# query = sys.argv[2]
query = "express"
print(query)
words = getWords(query, 2, 20)
print(words)
