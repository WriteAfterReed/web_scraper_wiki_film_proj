# Learning to Crawl

This is a fun side project for learning how to use scrapy to scrape and webcrawl.
Simple Flask app also included to just serve up basic templates if you hit a url.

Basically just goes to wikipedia starting from a few actors pages and makes a huge json file storing relations.

Sources:
Referred to http://pybae.github.io/blog/2015/04/27/a-simple-introduction-to-scrapy/ for inspiration. 


To run:

Requirements:  

    - Bs4  
    - scrapy
    - requests
    - json
    

To use the scrapy run:  

    scrapy crawl film_wiki_spider -o out.json
    
To run the graph tests run:  

    python3 graph_constructor.py
    


