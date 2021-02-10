import pandas as pd
import numpy as np

from bertopic import BERTopic


class BERTopicModel():
    """A Topic modelling model based on BERT
    """

    def __init__(self, n_topics="auto", model=None):
        """
        Parameters
        ----------
        n_topics : str/int, optional
            Number of topics to use, by default "auto"
        model : str, optional
            Existing model to load if any, by default None
        """
        if model is not None:
            print("> Using existing model")
            self.model = BERTopic.load(model)
            self.fitted = True
        else:
            self.model = BERTopic(nr_topics=n_topics)
            self.fitted = False
    

    def cluster_reviews(self, docs, n_topics_max=50):
        """Separates the reviews into different topics

        Parameters
        ----------
        docs : list[str]
            The reviews to cluster
        n_topics_max : int, optional
            maximum number of topics to use, by default 50

        Returns
        -------
        list
            topic indexes of each document
        """
        if not self.fitted:
            self.topics, self.probs = self.model.fit_transform(docs)
            self.fitted = True
        else:
            self.topics, self.probs = self.model.transform(docs)

        if len(self.model.get_topics()) > n_topics_max:
            self.topics, self.probs = self.model.reduce_topics(docs, self.topics, self.probs, nr_topics=n_topics_max)

        return self.topics
    

    def get_topics_description(self):
        """Gives the most frequent words for each identified topic
        """
        self.topics_desc = pd.DataFrame()
        for i in np.unique(self.topics):
            top_words = ", ".join([word[0] for word in self.model.get_topic(i)])
            self.topics_desc = self.topics_desc.append([[i, top_words]])
        self.topics_desc.reset_index(inplace=True, drop=True)
        self.topics_desc.columns = ["topic_idx", "top_words"]
        
        return self.topics_desc
    

    def save_model(self, path_save="./"):
        """Saves the trained model.

        Parameters
        ----------
        path_save : str, optional
            path where to save the model, by default "./"
        """
        self.model.save(f"{path_save}bertopic_model")


    

