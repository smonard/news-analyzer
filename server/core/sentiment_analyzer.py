from textblob import TextBlob
from classifier import SentimentClassifier
from collections import Counter
from sentiment_classifier import BasicSentimentClassifier

class SentimentAnalyzer:
    def __init__(self):
        self.__sent_py = SentimentClassifier()
        self.__nn_estimator = BasicSentimentClassifier.newinstance(context_path='../sentiment-estimator/data/')
        self.__nb_estimator = BasicSentimentClassifier.newinstance('nb', context_path='../sentiment-estimator/data/')
    
    def analyze(self, text, usetb=False):
        sentiment = (self.__nn_estimator.predict(text) + self.__nb_estimator.predict(text)) / 4.0
        sentiment += self.__sent_py.predict(text)
        estimators = 2.0
        if usetb:
            sentiment += self.__textblob_analysis(text)
            estimators += 1.0
        return self.__categorize(sentiment / estimators)
    
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
        
