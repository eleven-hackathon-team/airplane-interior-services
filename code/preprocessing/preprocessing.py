import pandas as pd
import re
import nltk
import numpy as np 
import spacy

from sentence_transformers import SentenceTransformer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


STOPWORDS = stopwords.words("english")


class Preprocessor():

    def __init__(self):
        self.data = None
    

    def _fetch_data(self, path_data="./", usecols=["comment"]):
        """Fetches and joins the scraped data.

        Parameters
        ----------
        path_data : str, optional
            Path where the data is located, by default "./"
        usecols : list, optional
            Columns to use, by default ["comment"]
        """
        print("> Fetching data")
        df_seatguru = pd.read_csv(f"{path_data}seatguru_reviews.csv", sep="|", usecols=usecols)
        df_skytrax = pd.read_csv(f"{path_data}skytrax_reviews.csv", sep="|", usecols=usecols)
        df_tripadvisor = pd.read_csv(f"{path_data}tripadvisor_reviews.csv", sep="|", usecols=usecols)

        self.data = pd.concat([df_seatguru, df_skytrax, df_tripadvisor], axis=0, ignore_index=True)
        self.data.drop(self.data.loc[self.data.comment.duplicated()].index, axis=0, inplace=True)
    

    def _filter_comments(self, min_length=0, max_length=np.inf):
        """Filters comments based on the number of characters

        Parameters
        ----------
        min_length : int, optional
            minimum length, by default 0
        max_length : int, optional
            maximum length, by default np.inf
        """
        print("> Filtering comments")
        self.data.drop(
            self.data.loc[self.data.comment.apply(lambda sentence: len(sentence)) < min_length].index,
            axis=0, 
            inplace=True
        )
        self.data.drop(
            self.data.loc[self.data.comment.apply(lambda sentence: len(sentence)) > max_length].index,
            axis=0, 
            inplace=True
        )


    def _clean_comments(self):
        """Lowers comments and removes special characters.
        """
        print("> Cleaning comments")
        self.data["comment_cleaned"] = self.data.comment.apply(lambda string: re.sub("[^a-z ]", "", string.lower()))


    def _remove_stopwords(self, stopwords=STOPWORDS):
        print("> Removing stopwords")
        self.data["comment_no_stopwords"] = self.data.comment_cleaned.apply(
            lambda sentence: " ".join([word for word in sentence.split(" ") if word not in stopwords])
        )


    def _lemmatize_comments(self, allowed_postags=['NOUN','ADJ','VERB','ADV']):
        """
        Parameters
        ----------
        allowed_postags : list[str], optional
            Type of tokens to keep, by default ['NOUN','ADJ','VERB','ADV']
        """
        print("> Lemmatizing comments")
        nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
        self.data["comment_lemmatized"] = self.data.comment_no_stopwords.apply(
            lambda sentence: " ".join([str(token) for token in nlp(sentence) if token.pos_ in allowed_postags])
        )


    def _embed(self, method="bert"):
        """Performs embedding on comments.

        Parameters
        ----------
        method : str, optional
            Model used to perform embedding, by default "bert"
        """
        if method == "bert":
            model = SentenceTransformer('distilbert-base-nli-mean-tokens')
            self.embeddings = model.encode(self.data.comment_cleaned.values, show_progress_bar=True)
        if method == "doc2vec":
            # TO DO
            return None


    def preprocess(self, path_data="./", usecols=["comment"], min_length=0, max_length=np.inf,
     stopwords=STOPWORDS, allowed_postags=['NOUN','ADJ','VERB','ADV']):
        """Fetches the data and preprocesses it.

        Parameters
        ----------
        path_data : str, optional
            Path where the data is located, by default "./"
        usecols : list, optional
            Columns to use, by default ["comment"]
        min_length : int, optional
            minimum length, by default 0
        max_length : int, optional
            maximum length, by default np.inf
        allowed_postags : list[str], optional
            Type of tokens to keep, by default ['NOUN','ADJ','VERB','ADV']

        Returns
        -------
        pandas.DataFrame
            The preprocessed data
        """
        self._fetch_data(path_data, usecols)
        self._filter_comments(min_length, max_length)
        self._clean_comments()
        self._remove_stopwords(stopwords)
        self._lemmatize_comments(allowed_postags)

        return self.data