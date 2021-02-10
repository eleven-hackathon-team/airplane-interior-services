from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



class VaderModel():
    """Baseline Sentiment Analysis model.
    """

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    

    def predict(self, sentence):
        score = self.analyzer.polarity_scores(sentence)["compound"]
        return score