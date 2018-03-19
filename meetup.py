#!flask/bin/python
from flask import Flask, Response
import json
import requests

from google.cloud import language
from google.cloud.language import enums, types

from google.protobuf.json_format import MessageToJson

app = Flask(__name__)

def get_tweets(input):
    tweets = requests.get('http://localhost:8080/twitter/tweets/' + input).json()
    return tweets

def analize_one_tweet(tweet):
    client = language.LanguageServiceClient()

    document = types.Document(
        language='en',
        content=tweet,
        type=enums.Document.Type.PLAIN_TEXT)

    annotations = client.analyze_sentiment(document=document, encoding_type='UTF32')

    return MessageToJson(annotations)


def analyze_all(input):
    tweet_list = get_tweets(input)
    #tweet_list = ['Maduro is bad', 'Maduro is good']
    result = []
    #print tweet_list
    for item in tweet_list:
        result.append(analize_one_tweet(item))
        
    #result = analize_one_tweet('Maduro is bad')
    #print result
    return result
    #return list(map(lambda item: analize_one_tweet(item), tweet_list))
    



@app.route('/meetup/api/v1/sentiments/<string:selector>', methods=['GET'])
def get_sentiments(selector):
    #print len(get_tweets('nintendo'))
#    return Response(json.dumps(get_tweets('nintendo')), mimetype='application/json')
    return Response(json.dumps({'sentiments': analyze_all(selector)}), mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True)
