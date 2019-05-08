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
We first used beautifulsoup

## Usages
### Dependencies
[metapy](https://pypi.org/project/metapy/)
[numpy](https://pypi.org/project/numpy/)
[Flask](https://pypi.org/project/Flask/)

### How to setup & run the App
Our project has a web-based user interface. We have deployed it on https://metapypy.herokuapp.com/ so you can directly use it.

If you want to test it locally, you need to install the dependencies and run `python app.py` in the frontend folder.

This will open a flask server and you will be able to see the website at `http://localhost:5000`.

## Work Distribution
Chen Pan: Frontend website UI design & implementation

Meishan Wu: Implemented the Text Mining Algorithms for our project

Zhonghao Pan: Scraping data from NPM Website


