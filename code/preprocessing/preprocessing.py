import pandas as pd
import re



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
        df_seatguru = pd.read_csv(f"{path_data}seatguru_reviews.csv", sep="|", usecols=usecols)
        df_skytrax = pd.read_csv(f"{path_data}skytrax_reviews.csv", sep="|", usecols=usecols)
        df_tripadvisor = pd.read_csv(f"{path_data}tripadvisor_reviews.csv", sep="|", usecols=usecols)

        self.data = pd.concat([df_seatguru, df_skytrax, df_tripadvisor], axis=0, ignore_index=True)
    

    def _clean_comments(self, char_to_remove=[]):
        """Lowers comments and removes specified characters.

        Parameters
        ----------
        char_to_remove : list, optional
            Characters to remove, by default []
        """
        self.data.comment = self.data.comment.apply(lambda string: string.lower())
        if len(char_to_remove) > 0:
            self.data.comment = self.data.comment.apply(lambda string: re.sub(char_to_remove, "", string))
    

    def _tokenize(self, method="bert"):
        # TO DO
        return None
    

    def preprocess(self, path_data="./", usecols=["comment"], char_to_remove=[], tokenize=False, method="bert"):
        """Fetches the data, cleans it and, if specified, tokenizes it.

        Parameters
        ----------
        path_data : str, optional
            Path where the data is located, by default "./"
        usecols : list, optional
            Columns to use, by default ["comment"]
        char_to_remove : list, optional
            Characters to remove, by default []
        tokenize : bool, optional
            Whether to tokenize the data or not, by default False
        method : str, optional
            The method to use for tokenizing the data, by default "bert"

        Returns
        -------
        pandas.DataFrame
            The preprocessed data
        """
        self._fetch_data(path_data, usecols)
        self._clean_comments(char_to_remove)
        if tokenize:
            self._tokenize(method)
        return self.data