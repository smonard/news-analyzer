from domain.politics_media_analyzer import PoliticsMediaAnalizer
from flask import Flask, request
from flask_cors import CORS

APP = Flask('News Analyzer')
CORS(APP)

@APP.route('/analyze-provider/<provider>')
def analyze_provider(provider):
    return PoliticsMediaAnalizer().analyze_by_provider(provider)

@APP.route('/analyze-news')
def analyze_news():
    news_url = request.args.get('url', type = str)
    return PoliticsMediaAnalizer().analyze_single_news(news_url)
