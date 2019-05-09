# CS410 Final Project

## Proposal 
For the CS410 final project, our group will build a recommendation system that recommends ‘Node.js’ libraries to frontend React javascript developers. The basic idea is to crawl ‘package.json’ from popular GitHub repositories (have highest star count) about ‘React’. The project would be very helpful to frontend developers because there are tons of npm(node package manager) libraries online and developers may feel lost on deciding which libraries to use. This is very novel because Google doesn’t return any meaningful result in searching for similar projects. 

This project will probably include both content-based filtering system and collaborative filtering system. We will use the existing users’ ‘package.json’ as initialization text and a metric to judge the similarity between repositories. Users can then provides feedback on whether the libraries are related to their projects, and the model can then learn based on the user feedback. All data will be crawled from Github using similar approach as MP2. This project will be written in Python and mainly utilizes the ‘metapy’ library.

The result of the project can be judged by data crawling from some less popular GitHub repositories. We can randomly remove some libraries and see if the model can recommend those removed libraries. The minimum goal for this semester is to finish up the recommendation system using the top-1000 popular repositories about ‘React’. If time allows, we could crawl more data and build a better app.

## Functionalities
Our application helps Node.js developers to find the packages that they might be interested in. 
### Recommand by your current packages
In each Node.JS project there is a package.json file indicating the packages used in the project. In this mode we will take your current packages in your Node.js package.json file and use the PLSA algorithm to find the most related packages. 

### Recommand by keyword
Each package on NPM has a brief description of itself on the website. In this mode we will use text mining techniques to find the packages that is most related to your given keywords based on package descriptions.

## Implementation of our App
There are three parts of our project and each of us was in charge of one of them.
First, we scraped the package.json data from various NPM projects.
We first used beautifulsoup to scrape the top 100 popular pages of github using the search keyword "React". We got about 800 useful repo out of the scrape, and aquires about 800 package.json as our data. We parse the data into text file which contains 800 rows(document) each row has a list of npm lib(terms) that we scraped from package.json of each git repo. We also scrape the top 100 popular pages of npm site(www.npmjs.com) using keyword "React". We got over 1500 npm lib out of it, each contains the "name", "description", and "keywords". We store the data into a json file in the schema of {title:"React",des:"A wonder lib...",keyword:[frontend,...]}.
With the json we have for the package.json we scraped from github and the description data we scraped from NPM website, we first parse the data into a form that can be feed to a metapy functions. We use line corpus and unigram analyzer.
For the package recommendation, we use OkapiBM25 ranker to get the top 10 relevant documents. we treat each package.json we scraped from a github repository as one document, and each package name is a term. The query is the user's input package.json. The result we get are the most similar package.json comparing to the users. Then, the second step is to mine topics from the related package lists. Adapted from the PLSA algorithm we used in MP3, it will mine a number of topics from the top 10 documents. The number can be changed, but better to be larger than 1 since the 1 topic mining with PLSA depends on the occurence of each term. After we have the topic-word distributions, we can infer the most important packages in the topics mined from the top 10 package.json. Thus, we'll recommend those packages to the users if they are not in the user's query.
The recommendation based on the description is more straight forward. Each document is a combination of the packages's name and the description. Since descriptions are natural languages, we use the same set of stopwords as MP2. The user can query by keywords, which can be descriptive words, or simply the name. We'll use the query to rank the documents with OkapiBM25, and the top 20 packages are returned to the user.
## Usages
### Dependencies
##### Text Mining Dependencies
[metapy](https://pypi.org/project/metapy/)
[numpy](https://pypi.org/project/numpy/)
[Flask](https://pypi.org/project/Flask/)
[Flask-Cors](https://pypi.org/project/Flask-Cors/)
[gunicorn](https://pypi.org/project/gunicorn/)
[Jinja2](https://pypi.org/project/Jinja2/)
[pytoml](https://pypi.org/project/pytoml/)
##### Scraper Dependencies
[bs4](https://pypi.org/project/bs4/)
[selenium](https://pypi.org/project/selenium/)

### How to setup & run the App
Our project has a web-based user interface. We have deployed it on https://metapypy.herokuapp.com/ so you can directly use it.
The instructions and example inputs are included on the web page.
If you want to test it locally, you need to install the dependencies with `pip3 install -r requirement.txt` and run `python3 app.py` in the frontend folder. This will open a flask server and you will be able to see the website at `http://localhost:5000`.
Note that there is a issue in the flask webserver when running locally, which cause the scoring function to run forever (That means the code may not work locally). Here is a link to [Stack Overflow](https://stackoverflow.com/questions/53369759/flask-code-inside-a-app-route-fails-runs-forever-when-called-a-second-time) on this issue. We found that we can avoid this issue by deploying the app on heroku. 



## Work Distribution
Chen Pan: Frontend website UI design & implementation

Meishan Wu: Implemented the text mining algorithms for our project

Zhonghao Pan: Scraping data from NPM website, setup project structure (Flask + React).


