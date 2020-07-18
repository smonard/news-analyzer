from collections import Counter
from unidecode import unidecode
from core.sentiment_analyzer import SentimentAnalyzer

class NewsAnalyzer:
    def __init__(self, subject_details):
        self.__subject_details = subject_details
        self.__sentiment_analyzer = SentimentAnalyzer()
        
    def __filtering_criteria(self, phrase):
        keywords = self.__subject_details.keywordsincontext
        return max([key in unidecode(phrase) for key in keywords])

    def __split_text(self, news_chunk):
        return news_chunk.split('\n')
        
    def analyze(self, news, single=False):
        news_chunks = self.__split_text(news['content']) + [news['title']]
        analysis_units = list(filter(self.__filtering_criteria, news_chunks))
        analysis_units = [ unit.split('\n') for unit in analysis_units ]
        analysis_units = [ phrase for unit in analysis_units for phrase in unit ]
        representative_data = len(analysis_units) >= len(news_chunks) * 0.3
        unit_results = Counter(list(map(lambda unit: self.__sentiment_analyzer.analyze(unit, usetb=single), analysis_units)))
        position = unit_results.most_common()[0][0] if len(unit_results.most_common()) else 'non-analyzable'
        return { 'position': position, 
                 'provider': news['provider'],
                 'details': { k: v/len(analysis_units) for k, v in dict(unit_results).items() }, 
                 'representative': representative_data,
                 'analyzed': "{}/{}".format(len(analysis_units),len(news_chunks)) }
    