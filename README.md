<p align="center"><img src="img/logo.JPG"width=40%/></p>

===
Final project for [Data Mining](http://aris.me/index.php/data-mining-2016) course of MSc in Engineering in Computer Science
at Università degli Studi di Roma "La Sapienza" (A.Y. 2016/2017).

## The project
**Sentweements** is a simple sentiment analysis tool for tweets.
This visualisation allows you to see the Italian **sentimental situation**, using Twitter Streaming API to fetch tweets
coming from Italy in real-time and Indico artificial intelligence to perform a textual sentiment analysis. It is also
possible to select the starting date of the analysis, to get many different perspectives.
Results are presented in real-time on the client side in a beautiful fashion.
See also our images streaming [emotion analysis](https://github.com/giacomolanciano/sentweements).

## Technologies
- [Indico](https://indico.io/) - the artificial intelligence that detect sentiments in texts, available for several different languages.
- [Twitter Streaming API](https://dev.twitter.com/streaming/overview) - to access in real-time to tweets coming from all over the Italy.
- [Flask](http://flask.pocoo.org/) - microframework to build the webserver and serve client requests.
- [Leaflet](http://leafletjs.com/) - to build the dynamic visualisation of Italian regions.

## To run
Be sure to have **Python 3** installed. Note that some additional Python modules are required, you can run `dependencies.py`
to install them all in one shot.
To run the webapp (locally), open a terminal and type `$ python webapp.py`. Then, open a browser and go to
**localhost:5000**  (note that you still need a working Internet connection to download the tweets from Twitter).

<br><p align="center" href="https://gyazo.com/0eabb771ee5875242b2e473aef9ec40b"><img src="https://i.gyazo.com/0eabb771ee5875242b2e473aef9ec40b.gif" alt="https://gyazo.com/0eabb771ee5875242b2e473aef9ec40b" width="50%"/></p>

## Developers

|                |                                     |
|----------------|-------------------------------------|  
|Fabio Rosato    |rosato.1565173@studenti.uniroma1.it  |  
|Giacomo Lanciano|lanciano.1487019@studenti.uniroma1.it|  
