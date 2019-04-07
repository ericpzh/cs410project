# cs410project

#todo: grab data from ./scraper/.txt, use it in ./frontend/.py template

# proposal 
For the CS410 final project, our group will build a recommendation system that recommends ‘Node.js’ libraries to frontend React javascript developers. The basic idea is to crawl ‘package.json’ from popular GitHub repositories (have highest star count) about ‘React’. The project would be very helpful to frontend developers because there are tons of npm(node package manager) libraries online and developers may feel lost on deciding which libraries to use. This is very novel because Google doesn’t return any meaningful result in searching for similar projects. 
This project will probably include both content-based filtering system and collaborative filtering system. We will use the existing users’ ‘package.json’ as initialization text and a metric to judge the similarity between repositories. Users can then provides feedback on whether the libraries are related to their projects, and the model can then learn based on the user feedback. All data will be crawled from Github using similar approach as MP2. This project will be written in Python and mainly utilizes the ‘metapy’ library.
The result of the project can be judged by data crawling from some less popular GitHub repositories. We can randomly remove some libraries and see if the model can recommend those removed libraries. The minimum goal for this semester is to finish up the recommendation system using the top-1000 popular repositories about ‘React’. If time allows, we could crawl more data and build a better app.
