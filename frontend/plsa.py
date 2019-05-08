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
    # print("Vocabulary size:" + str(len(corpus.vocabulary)))
    # print("Number of documents:" + str(len(corpus.documents)))
    max_iterations = 50
    epsilon = 0.01
    l = corpus.plsa(number_of_topics, max_iterations, epsilon)
    ret = []
    for score, term in l:
        if term not in ret and term not in query:
            ret.append(term)
        if len(ret) > number_of_terms:
            break
    return ret

# doc = [' body parser express scripts test start ', '  babel core  babel plugin syntax dynamic import  babel preset env  babel preset react  babel register  start cli  start plugin env  start plugin find  start plugin lib babel  start plugin lib codecov  start plugin lib eslint  start plugin lib jest  start plugin lib webpack serve  start plugin parallel  start plugin read  start plugin remove  start plugin sequence  start plugin write  start reporter verbose  start task babel core babel eslint babel jest babel loader enzyme enzyme adapter react 16 enzyme to json eslint eslint config standard eslint config standard react eslint plugin import eslint plugin node eslint plugin promise eslint plugin react eslint plugin standard html webpack plugin metro react native babel preset raf react react dom react hot loader react test renderer recompose webpack ', ' express  bahmutov print env bluebird chalk console table cypress del figlet gulp gulp autoprefixer gulp cache gulp if gulp imagemin gulp jshint gulp load plugins gulp rename gulp replace gulp size gulp uncss gulp useref gulp vulcanize jshint stylish minimist npm run all pluralize psi ramda run sequence serve favicon start server and test vinyl fs ', ' react  babel runtime compute scroll into view prop types react is  babel helpers  types react babel plugin macros babel preset react native buble cpy cli cross env cypress cypress testing library docz docz theme default eslint plugin cypress flow bin flow coverage report jest dom kcd scripts npm run all preact preact render to string react react dom react native react test renderer react testing library rollup plugin commonjs serve start server and test typescript ', ' main module jsnext main types files build types  scripts build lint start test test coverage test watch test ci prop types react  types jest  types prop types  types react  types react dom awesome typescript loader babel cli babel eslint babel jest babel preset es2015 babel preset react babel preset typescript codecov eslint eslint plugin shopify fs extra jest nwb react react addons test utils react dom react test renderer rimraf rollup rollup plugin babel rollup plugin commonjs rollup plugin node resolve rollup plugin typescript2 rollup plugin uglify tslint tslint config shopify typescript ', '  babel cli  babel core  babel plugin proposal class properties  babel plugin proposal export default from  babel plugin proposal object rest spread  babel preset env  babel preset react all contributors cli babel core babel eslint babel jest babel loader babel plugin emotion babel plugin inline svg babel plugin lodash babel plugin module resolver babel plugin transform builtin extend babel plugin transform export extensions babel plugin transform inline environment variables cache me outside cross env cypress dom testing library eslint eslint plugin react friendly errors webpack plugin http server jest jest cli jest emotion lerna npm run all prettier react test renderer rimraf start server and test stylelint stylelint config recommended stylelint config styled components stylelint processor styled components svg inline loader ', ' scripts start test build docs build clean docz dev docz build  babel core  babel plugin proposal class properties  babel plugin proposal decorators  babel plugin proposal object rest spread  babel preset env  babel preset react  babel preset typescript  smooth ui core sc  types jest  types react  types react dom  types react kawaii  types react sparklines  types styled components  types webpack babel core babel jest babel loader babel plugin external helpers babel preset env babel preset react babel preset stage 0 cross env css loader docz file loader html webpack plugin html webpack template jest react react color react compound slider react dom react feather react json view react kawaii react popper react sparklines react testing library rimraf style loader styled components typeface nunito typescript url loader webpack webpack cli webpack dev server react react dom ', ' dist win x64 pack win test test setup test integration test unit react test unit react watch test unit react coverage test unit browser test unit test unit main upload dist fix lint fix lint browser fix lint cli fix lint main fix lint test lint lint browser lint cli lint main lint test pack ccov instrument ccov test browser ccov remap browser html ccov remap browser lcov ccov clean ccov upload jest ccov upload launch start start hot start not dev watch browser watch plugins watch plugins oni plugin typescript watch plugins oni plugin markdown preview watch plugins oni plugin git watch plugins oni plugin quickopen install plugins install plugins oni plugin markdown preview install plugins oni plugin prettier install plugins oni plugin git postinstall profile webpack  githubprimer octicons react chokidar color normalize dompurify electron settings find up font manager fs extra highlight js json5 keyboard layout marked minimist msgpack lite ocaml language server oni api oni fontkit oni neovim binaries oni ripgrep oni types react react dnd react dnd html5 backend react dom redux batched subscribe shell env shelljs simple git styled components typescript vscode css languageserver bin vscode html languageserver bin vscode jsonrpc vscode languageserver vscode languageserver types vscode textmate  types chokidar  types color  types detect indent  types dompurify  types electron settings  types enzyme  types fs extra  types highlight js  types jest  types jsdom  types json5  types lodash  types lolex  types marked  types minimatch  types minimist  types mkdirp  types mocha  types msgpack lite  types node  types react  types react dnd  types react dnd html5 backend  types react dom  types react motion  types react redux  types react test renderer  types react transition group  types react virtualized  types redux batched subscribe  types redux mock store  types rimraf  types shelljs  types sinon  types webgl2 autoprefixer aws sdk azure storage babel minify webpack plugin babel plugin dynamic import node bs platform codecov color concurrently cross env css loader detect indent electron electron builder electron devtools installer electron mocha electron rebuild enzyme enzyme adapter react 16 enzyme to json extract zip find process fuse js github releases html loader husky innosetup compiler istanbul api istanbul lib coverage jest jest styled components jsdom less less loader less plugin autoprefix lodash lolex memory fs minimatch mkdirp mocha node abi npm run all nyc oni core logging oni release downloader opencollective prettier pretty quick react hot loader react motion react redux react test renderer react transition group react virtualized redux redux mock store redux observable redux thunk remap istanbul reselect rxjs sinon spectron style loader sudo prompt ts jest ts loader tslint typescript plugin styled components vscode snippet parser wcwidth webdriverio webpack webpack bundle analyzer webpack cli webpack dev server ', ' apollo cache inmemory apollo client apollo fetch apollo link http apollo server express babel runtime body parser cookie cookie parser debug dotenv express express session firebase graphql graphql tag graphql tools isomorphic fetch lru cache next passport passport local prop types react react apollo react dom react render html url babel cli babel core babel eslint babel jest babel loader babel preset env babel preset react babel preset stage 0 enzyme enzyme adapter react 16 enzyme to json eslint eslint config airbnb eslint plugin import eslint plugin jsx a11y eslint plugin react jest jest enzyme mockdate nodemon react test renderer ', ' prop types babel cli babel loader babel plugin dynamic import node babel plugin module resolver babel plugin transform async to generator babel plugin transform class properties babel plugin transform object assign babel preset es2015 babel preset react express flow bin jest react react dom react test renderer webpack react ']
# query = "express start test babel"
# topicWords(doc, query, 2, 20)
