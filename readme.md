# TwittMap

TwittMap is an online website that allows users to search tweets that contain a certain keyword in real-time.

## Dependence

Django 1.9.2

elasticsearch 

elasticsearch_dsl

requests_aws4auth

tweepy


## Usage

Originally, you will see an empty Google Map and the Google Street View of the Times Square.

Type something and click search. It will search tweets posted recently (30 minutes in our application).

If there are no tweet posted recently containing this keyword, the web will tell you there is no result. 

Else you will see the tweets as markers on the Google Map where they are posted. Click a marker and you will see the user who posted this tweet and the content of the tweet.

As for the keywords, it is quite usual that there is no tweets posted recently containing a certain keyword. However, if you choose an arbitary word, e.g. 'the', there will be a lot of tweets containing it.