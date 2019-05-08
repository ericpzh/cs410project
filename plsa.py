import numpy as np
import math


def normalize(input_matrix):
    """
    Normalizes the rows of a 2d input_matrix so they sum to 1
    """

    row_sums = input_matrix.sum(axis=1)
    assert (np.count_nonzero(row_sums)==np.shape(row_sums)[0]) # no row should sum to zero
    new_matrix = input_matrix / row_sums[:, np.newaxis]
    return new_matrix


class Corpus(object):

    def __init__(self):
        """
        Initialize empty document list.
        """
        self.documents = []
        self.vocabulary = []
        self.likelihoods = []
        self.term_doc_matrix = None
        self.document_topic_prob = None  # P(z | d)
        self.topic_word_prob = None  # P(w | z)
        self.topic_prob = None  # P(z | d, w)
        self.number_of_documents = 0
        self.vocabulary_size = 0

    def build_corpus(self, documents):
        """
        Read document, fill in self.documents, a list of list of word
        self.documents = [["the", "day", "is", "nice", "the", ...], [], []...]

        Update self.number_of_documents
        """

        for j in range(len(documents)):
            documents[j] = [i.strip() for i in documents[j].split()]
        self.documents = documents
        self.number_of_documents = len(self.documents)


    def build_vocabulary(self):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]

        Update self.vocabulary_size
        """
        # #############################
        # your code here
        self.vocabulary = list(set(sum(self.documents, [])))
        self.vocabulary_size = len(self.vocabulary)
        # #############################

        # pass    # REMOVE THIS

    def build_term_doc_matrix(self):
        """
        Construct the term-document matrix where each row represents a document,
        and each column represents a vocabulary term.

        self.term_doc_matrix[i][j] is the count of term j in document i
        """
        # ############################
        # your code here
        self.term_doc_matrix = np.zeros((self.number_of_documents, self.vocabulary_size))
        for i in range(self.number_of_documents):
            for j in range(self.vocabulary_size):
                self.term_doc_matrix[i][j] = self.documents[i].count(self.vocabulary[j])
        # ############################

        # pass    # REMOVE THIS


    def initialize_randomly(self, number_of_topics):
        """
        Randomly initialize the matrices: document_topic_prob and topic_word_prob
        which hold the probability distributions for P(z | d) and P(w | z): self.document_topic_prob, and self.topic_word_prob

        Don't forget to normalize!
        """
        # ############################
        # your code here
        self.document_topic_prob = np.random.rand(self.number_of_documents, number_of_topics)
        self.document_topic_prob = normalize(self.document_topic_prob)

        self.topic_word_prob = np.random.rand(number_of_topics, self.vocabulary_size)
        self.topic_word_prob = normalize(self.topic_word_prob)
        # ############################

        # pass    # REMOVE THIS


    def initialize_uniformly(self, number_of_topics):
        """
        Initializes the matrices: self.document_topic_prob and self.topic_word_prob with a uniform
        probability distribution. This is used for testing purposes.

        DO NOT CHANGE THIS FUNCTION
        """
        self.document_topic_prob = np.ones((self.number_of_documents, number_of_topics))
        self.document_topic_prob = normalize(self.document_topic_prob)

        self.topic_word_prob = np.ones((number_of_topics, len(self.vocabulary)))
        self.topic_word_prob = normalize(self.topic_word_prob)

    def initialize(self, number_of_topics, random=False):
        """ Call the functions to initialize the matrices document_topic_prob and topic_word_prob
        """
        if random:
            self.initialize_randomly(number_of_topics)
        else:
            self.initialize_uniformly(number_of_topics)

    def expectation_step(self):
        d = self.number_of_documents
        z = self.topic_word_prob.shape[0]
        w = self.vocabulary_size
        self.topic_prob = self.document_topic_prob.T.reshape(z, d, 1) * self.topic_word_prob.reshape(z, 1, w)
        self.topic_prob = self.topic_prob / np.sum(self.topic_prob, axis = 0)


    def maximization_step(self, number_of_topics):
        self.topic_word_prob = np.sum(self.topic_prob * self.term_doc_matrix, axis=1)
        self.topic_word_prob = self.topic_word_prob / np.sum(self.topic_word_prob, axis=1).reshape(number_of_topics, 1)

        self.document_topic_prob = np.sum(self.topic_prob * self.term_doc_matrix, axis=2).T
        self.document_topic_prob = self.document_topic_prob / np.sum(self.document_topic_prob, axis = 1).reshape(self.number_of_documents, 1)


    def calculate_likelihood(self, number_of_topics):
        """ Calculate the current log-likelihood of the model using
        the model's updated probability matrices

        Append the calculated log-likelihood to self.likelihoods

        """
        d = self.number_of_documents
        z = number_of_topics
        w = self.vocabulary_size
        likelihood = np.sum(np.log(np.sum(self.document_topic_prob.T.reshape(z, d, 1) * self.topic_word_prob.reshape(z, 1, w), axis = 0)) * self.term_doc_matrix)
        self.likelihoods.append(likelihood)
        return

    def plsa(self, number_of_topics, max_iter, epsilon):
        # build term-doc matrix
        self.build_term_doc_matrix()
        # Create the counter arrays.
        # P(z | d, w)
        self.topic_prob = np.zeros([number_of_topics, self.number_of_documents, self.vocabulary_size], dtype=np.float)
        # P(z | d) P(w | z)
        self.initialize(number_of_topics, random=True)
        # Run the EM algorithm
        current_likelihood = 0.0
        for iteration in range(max_iter):
            oldpi = self.document_topic_prob.copy()
            self.expectation_step()
            self.maximization_step(number_of_topics)
            self.calculate_likelihood(number_of_topics)
            if len(self.likelihoods) >= 2 and (abs(self.likelihoods[-1] - self.likelihoods[-2]) < epsilon):
                break
        l = []
        for i in range(number_of_topics):
            l += [j for j in zip(self.topic_word_prob[i], self.vocabulary)]
        l.sort(key = lambda t: t[0], reverse = True)
        return l
def topicWords(doc, query, number_of_topics=3, number_of_terms=10):
    corpus = Corpus()
    corpus.build_corpus(doc)
    corpus.build_vocabulary()
    max_iterations = 50
    epsilon = 0.01
    l = corpus.plsa(number_of_topics, max_iterations, epsilon)
    ret = []
    for score, term in l:
        if term not in ret and term not in query:
            ret.append(term)
        if len(ret) >= number_of_terms:
            break
    return ret
