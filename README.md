<p align="center"><img src="img/logo.JPG"width=40%/></p>

===
Final project for [Data Mining](http://aris.me/index.php/data-mining-2016) course of MSc in Engineering in Computer Science
at Università degli Studi di Roma "La Sapienza" (A.Y. 2016/2017).

## The project
**Sentweements** is a simple sentiment analysis tool for tweets. It allows you to make a query against
[Twitter Search API](https://dev.twitter.com/rest/public) and get back a dynamic sentiment analysis. It builds an image
stream from the incoming tweets, performs sentiment analysis of each image using
[Microsoft Emotion API](https://www.microsoft.com/cognitive-services/en-us/emotion-api) and push it to the web client.
Results are presented on the client side in a beautiful fashion.
See also our text streaming [sentiment analysis](https://github.com/giacomolanciano/sentweements/tree/master-v2).

## Technologies
- Microsoft Emotion API - the artificial intelligence that detect emotions based on universal facial expressions.
- Twitter Search API - give access to indices of recent or popular Tweets.
- [Flask](http://flask.pocoo.org/) - microframework to build the webserver and serve client requests.
- [SocketIO](http://socket.io/) - to build the pub-sub system to push notifications between client and server.

## To run
Be sure to have **Python 3** installed. Note that some additional Python modules are required.  
To run the webapp (locally), open a terminal and type `$ python webapp.py`. Then, open a browser and go to
**localhost:5000**  (note that you still need a working Internet connection to download the tweets from Twitter).

## Developers

|                  |                                     |
|------------------|-------------------------------------|  
|Fabio Rosato      |rosato.1565173@studenti.uniroma1.it  |  
|Giacomo Lanciano  |lanciano.1487019@studenti.uniroma1.it|  
|Francisco Ferreres|matakukos@gmail.com                  |   
