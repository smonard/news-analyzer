from textblob import TextBlob
from classifier import SentimentClassifier
from pycorenlp import StanfordCoreNLP
from collections import Counter

class SentimentAnalyzer:
    def __init__(self):
        self.__clf = SentimentClassifier()
    
    def analyze(self, text, usetb=False):
        sentiment = self.__clf.predict(text)
        if usetb:
            sentiment = (sentiment + self.__textblob_analysis(text)) / 2.00
        return self.__categorize(sentiment)
    
    def __textblob_analysis(self, text):
        sentiment = TextBlob(text).translate(to='en').sentiment
        if sentiment.polarity == 0:
            return 0.5
        sign = sentiment.polarity / abs(sentiment.polarity)
        sentiment_value = (abs(sentiment.polarity) + 0.15 * pow(sentiment.subjectivity, 2))
        return ((sign * sentiment_value) + 1.15) / 2.3

    def __categorize(self, rate):
        classes = {0: 'negative', 1:'neutral', 2: 'positive', 3: 'positive'}
        return classes[round(rate/0.5)]
        
