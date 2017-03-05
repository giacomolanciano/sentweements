<p align="center"><img src="img/logo.JPG"width=40%/></p>

===
Final project for [Data Mining](http://aris.me/index.php/data-mining-2016) course of MSc in Engineering in Computer Science
at Università degli Studi di Roma "La Sapienza" (A.Y. 2016/2017).

## The project
**Sentweements** is a beautifully intuitive sentiment analysis tool for tweets.

Using Twitter Streaming API to fetch tweets in real-time and Indico's artificial intelligence APIs to perform textual sentiment analysis, data is visualized on a beautiful, interactive choropleth map showing Italy's **sentimental situation**.

With **Sentweements** you have:
- national and region-specific statistics, available through mouse hover.
- data persistence implemented with [SQLite DB](https://www.sqlite.org/).
- dynamic updates automatically reflected on the map as new data becomes available (Twitter streaming data).
- static analysis mode available by defining a time window of tweets to analyze, to get different perspectives.
- api keys **carousel** and **multi-threaded** data retrieval architecture to expand rate limit both for Twitter and sentiments APIs (check [secret_keys_template](
https://github.com/giacomolanciano/sentweements/blob/master-v2/secret_keys_template.txt) for instructions).

See also our images streaming [emotion analysis](https://github.com/giacomolanciano/sentweements).

## Technologies
- [Indico](https://indico.io/) - an artificial intelligence service that detects sentiments in texts, available for several different languages.
- [Twitter Streaming API](https://dev.twitter.com/streaming/overview) - real-time access to tweets coming from all over Italy.
- [Flask](http://flask.pocoo.org/) - Python microframework to build the webserver and serve client requests.
- [Leaflet](http://leafletjs.com/) - Javascript framework to build the choropleth map visualization.

## To run
Be sure to have **Python 3** installed.

Note that some additional Python modules are required; you can run `$ python dependencies.py`
to install them all in one shot.

To start tweets retrieval, open a terminal and type `$ python tweets_streaming.py`.  
Note that you need a working Internet connection to download the tweets from Twitter.

To run the webapp (locally), open a terminal and type `$ python webapp.py`.  
Then, open a browser and go to **localhost:5000**.

<br /><p align="center" href="https://gyazo.com/0eabb771ee5875242b2e473aef9ec40b"><img src="https://gyazo.com/6c0e91ecbe89f09a7227677c23854327.gif" alt="https://gyazo.com/6c0e91ecbe89f09a7227677c23854327" width="50%"/></p><br />

## Developers

|                |                                     |
|----------------|-------------------------------------|  
|Fabio Rosato    |rosato.1565173@studenti.uniroma1.it  |  
|Giacomo Lanciano|lanciano.1487019@studenti.uniroma1.it|  
