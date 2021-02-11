from textblob import TextBlob


class TextblobModel():
    """Textblob-based sentiment analysis model.
    """

    def __init__(self):
        self.model = TextBlob
    

    def predict(self, sentence):
        score = self.model(sentence).sentiment.polarity

        return score