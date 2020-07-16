from collections import Counter
from unidecode import unidecode
from domain.news_analyzer import NewsAnalyzer
from domain.analysis_subject_details import AnalysisSubjectDetails
from dataloader.source_loader import FileSourceLoader, HttpSourceLoader

class PoliticsMediaAnalizer:
    def __init__(self):
        self.__subject_details = AnalysisSubjectDetails()
        self.__news_analyzer = NewsAnalyzer(self.__subject_details)
        self.__translations = { 'neutral': 'Neutral', 'positive': 'Supporter', 'negative': 'Opponent' }
        
    def __switch_source_loader(self, loader_key):
        self.__source_loader = HttpSourceLoader() if loader_key == 'http' else FileSourceLoader()
        
    def __filtering_criteria(self, news):
        keywords = self.__subject_details.contextidentifiers
        return max([key in unidecode(news['title']) or key in unidecode(news['content']) for key in keywords])

    def __clean_data(self, raw_data):
        for news in raw_data:
            news['title'] = news['title'].lower()
            news['content'] = news['content'].lower()
        return raw_data
    
    def analyze_by_provider(self, provider):
        self.__switch_source_loader('file')
        raw_data = self.__source_loader.load(provider)
        data = list(filter(self.__filtering_criteria, self.__clean_data(raw_data)))
        results = [self.__news_analyzer.analyze(news) for news in data]
        representative_analysis = [ r['position'] for r in filter(lambda result: result['representative'], results) ]
        final_analysis = Counter(representative_analysis)
        return { 'provider': raw_data[0]['provider'], # May throw an exception if no data
                 'position': self.__translations[final_analysis.most_common()[0][0]],
                 'details': { k: v/len(representative_analysis) for k, v in dict(final_analysis).items() },
                 'analyzed': "{}/{}".format(len(representative_analysis), len(data)) }
    
    def analyze_single_news(self, url):
        self.__switch_source_loader('http')
        news = self.__clean_data([self.__source_loader.load(url)])[0]
        result = self.__news_analyzer.analyze(news, True)
        result['position'] = self.__translations[result['position']]
        return result


