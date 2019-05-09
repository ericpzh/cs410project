import math
import sys
import time
import metapy
import pytoml
import json
from plsa import topicWords
class PackageSearcher:
    """
    Class PackageSearcher
    Recommend packages based on similar package.json
    Attributes:
    idx: a inverted index that can be loaded directly
    ranker: OkapiBM25 ranker
    documents: the entire data that we scraped from github
    """
    def __init__(self, cfg):
        self.idx = metapy.index.make_inverted_index(cfg)
        self.ranker = metapy.index.OkapiBM25()
        with open("package/package.dat", 'r') as f:
            documents = []
            for i in f.readlines():
                documents.append(i.replace('\n', ''))
        self.documents = documents

    def search(self, queryContent, number_of_topics=3, number_of_terms=20):
        """
        Call metapy ranker and scoring fuctions and PLSA to return recomendations
        :param:queryContent: A space seperated string, each is a package name
        """
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
    """
    Class DescriptionSearcher
    Search packages based descriptions
    Attributes:
    idx: a inverted index that can be loaded directly
    ranker: OkapiBM25 ranker
    documents: parsed document
    packages: the original json data
    """
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


    def search(self, queryContent):
        """
        Call metapy ranker and scoring fuctions to return recomendations
        :param:queryContent: A space seperated string, each is a keyword
        """
        query = metapy.index.Document()
        query.content(queryContent)
        ranker = self.ranker
        query = metapy.index.Document()
        query.content(queryContent)
        results = ranker.score(self.idx, query, 20)
        print("get result", results)
        rel_doc = []
        for id, score in results:
            rel_doc.append(self.packages[id])
        return rel_doc
