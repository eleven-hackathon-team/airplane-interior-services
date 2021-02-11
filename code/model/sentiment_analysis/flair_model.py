import flair


class FlairModel():
    """A sentiment analysis model based on Flair's sentiment classifier
    """

    def __init__(self):
        self.model = flair.models.TextClassifier.load('en-sentiment')
    

    def predict(self, sentence):
        s = flair.data.Sentence(sentence)
        self.model.predict(s)
        
        label = str(s.labels[0]).split(" ")
        sentiment = label[0]
        abs_score = float(label[1].replace("(", "").replace(")", ""))
        score = (1*(sentiment=="POSITIVE") - 1*(sentiment=="NEGATIVE"))*abs_score

        return score